import numpy as np
import random
from player import Player

class QPlayer(Player):
    # state: 00 = empty, 01 = move home, 10 = move empty, 11 = move
    def __init__(self, pid, lr, disc, eps):
        Player.__init__(self, pid)
        self.train = True
        self.lr = lr
        self.disc = disc
        self.eps = eps
        self.verbose = False
        self.state = [0,0,0,0,0,0]
        self.EMPTY = 0
        self.HOME = 1
        self.CAPTURE = 2
        self.NEXT = 3
        self.THREAT = 4
        self.Q = np.zeros((8**6,6))
        self.actions = [] # action replay buffer
        self.states = [] # state replay buffer
        self.rewards = [] # reward replay buffer
        #print('Q shape:', np.shape(self.Q))
        
    def resetActions(self):
        self.actions = []
        
    def resetStates(self):
        self.states = []
        
    def resetRewards(self):
        self.rewards = []
        
    def seteps(self, eps):
        self.eps = eps

    def statetoidx(self, state):
        # compresses list of states to integer 0-6**8
        idx = 0
        mult = 1
        for pos in state:
            idx += pos*mult
            mult *= 8
        return int(idx)
        
    def getmaxQ(self, board):
        idx = self.statetoidx(self.state)
        qmax = np.amax(self.Q[idx])
        return qmax
        
    def calcreward(self, a, board):
        pit = a+1
        seeds = board.pits[pit]
        dest = int((pit - seeds) % 14)
        reward = 0
        if seeds == 0: # illegal move pit empty
            reward -= 3
        if seeds == pit: # home, extra move
            reward += 3
        if seeds > pit: # one stone added
            reward += 1
        if (seeds > 0) and (board.pits[dest] == 0) and dest in self.valid_pits:
            reward += board.pits[(dest-7)%14] + 1
        if self.state[a] & 4: # threatened
            reward += board.pits[pit] + 1

        return reward
        
    def pickQpit2(self, board):
        if random.random()<self.eps:
            pit = random.randint(1,6)
            if self.verbose:
                print('random pit', pit)
            return pit
        else:
            # convert Q to probs
            idx = self.statetoidx(self.state)
            if np.sum(self.Q[idx]) == 0:
                pit = random.randint(1,6) # equal probs
            else:
                probs = self.Q[idx]/np.sum(self.Q[idx])
                pit = int(np.random.choice(6, 1, p=probs)) + 1
            if self.verbose:
                print(pit, idx, np.array_str(self.Q[idx], precision=2))
            return pit

    def pickQpit(self, board):
        self.update_state(board)
        if random.random()<self.eps:
            #print('random pit')
            return random.randint(1,6)
        else:
            #print('maxQ pit')
            idx = self.statetoidx(self.state)
            #Q_copy = self.Q[idx].copy()
            allowed_moves = board.allowed_moves()
            #print('allowed moves:', allowed_moves)
            if len(allowed_moves) == 1:
                return allowed_moves[0]
            offset = board.homes[board.player]
            moves_and_scores = []
            for move in board.allowed_moves():
                moves_and_scores.append([move, self.Q[idx][move-offset-1]])
            #pit = np.argmax(self.Q[idx]) + 1
            scores = [item[1] for item in moves_and_scores]
            max_score = max(scores)

            potential_moves = []
            for move_and_score in moves_and_scores:
                if move_and_score[1] == max_score:
                    potential_moves.append(move_and_score[0])
            #print('potential moves:', potential_moves)

            pit = random.choice(potential_moves)
            if self.verbose:
                print(pit, idx, np.array_str(self.Q[idx], precision=2))
            return pit
    
    def update_state(self, board):
            
        for pit in self.valid_pits:
            seeds = board.pits[pit]
            dest = int((pit - seeds) % 14)
            threatened = False
            if board.pits[pit] != 0 and board.pits[(14-pit)] == 0: # opposite pit empty
                for ipit in self.invalid_pits:
                    if (ipit + pit) != 14: # check all but opposite for CAPTURE
                        iseeds = board.pits[ipit]
                        idest = int((ipit - iseeds) % 14)
                        if idest == (14-pit):
                            threatened = True
            #print('dest = ', dest)
            if seeds == 0:
                self.state[pit-1] = self.EMPTY
            elif seeds == pit:
                self.state[pit-1] = self.HOME
            elif (board.pits[dest] == 0) and dest in self.valid_pits:
                self.state[pit-1] = self.CAPTURE
            else:
                self.state[pit-1] = self.NEXT
            if threatened:
                self.state[pit-1] += self.THREAT
        #print('state = ', self.state)
            

    def updateQ(self, s, a, r, maxQ):
        #print('prior Q[',s,a,'] =',s,a,self.Q[s,a])
        self.Q[s,a] = (1-self.lr)*self.Q[s,a]+self.lr*r+self.lr*self.disc*maxQ
        #print('post Q[',s,a,'] =',s,a,self.Q[s,a])
        
    def updateQ2(self, states, actions, rewards):
        #print('Updating Qs')
        rdisc = []
        R = 0
        for r in rewards[::-1]:
            # calculate the discounted rewards
            R = r + self.disc * R
            rdisc.insert(0, R)
        #print('states', states)
        #print('actions', actions)
        #print('rewards', rewards)
            
        for state, a, r, R in zip(states, actions, rewards, rdisc):
            s = self.statetoidx(state)
            #print(s, a, np.array_str(self.Q[s], precision=2))
            self.Q[s,a] = (1-self.lr)*self.Q[s,a]+self.lr*r+self.lr*R
            #print(s, a, np.array_str(self.Q[s], precision=2))

    def get_move(self, board):
        self.update_state(board)
        pit = self.pickQpit(board)
        reward = self.calcreward(pit-1, board)
        self.actions.append(pit-1)
        #print('actions', self.actions)
        self.rewards.append(reward)
        #print('rewards', self.rewards)
        self.states.append(self.state.copy())
        #self.update_state(board)
        return pit
