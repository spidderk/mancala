from player import Player

class GreedyPlayer(Player):
    # state: 00 = empty, 01 = move home, 10 = move empty, 11 = move
    def __init__(self, pid):
        Player.__init__(self, pid)
        self.state = [0,0,0,0,0,0]
        self.EMPTY = 0
        self.HOME = 1
        self.CAPTURE = 2
        self.NEXT = 3
        

    def update_state(self, board):
            
        for pit in self.valid_pits:
            seeds = board.pits[pit]
            dest = int((pit - seeds) % 14)
            #print('dest = ', dest)
            if seeds == 0:
                self.state[pit%7-1] = self.EMPTY
            elif seeds == pit%7:
                self.state[pit%7-1] = self.HOME
            elif (board.pits[dest] == 0) and dest in self.valid_pits:
                self.state[pit%7-1] = self.CAPTURE
            else:
                self.state[pit%7-1] = self.NEXT
            #print('state = ', self.state)
    
    def pickGreedypit(self, board):
        self.update_state(board)
        if self.pid == 'P2':
            offset = 7
        else:
            offset = 0
        for index in range(len(self.state)):
            pit = index + offset + 1
            if self.state[index] == self.HOME:
                return pit
        for index in range(len(self.state)):
            pit = index + offset + 1
            if self.state[index] == self.CAPTURE:
                return pit
        for index in range(len(self.state)):
            pit = index + offset + 1
            if self.state[index] != self.EMPTY:
                return pit

        return pit
                
    def get_move(self, board):
        #print(self.pid, "turn (Greedy)")
        return self.pickGreedypit(board)
    
#    def turn(self, board):
#        turnNotDone = True
#        #print(self.pid, "turn (Greedy)")
#        while turnNotDone and not(board.check_done()):
#            pit = self.pickGreedypit(board)
#            turnNotDone = self.move(pit, board)
