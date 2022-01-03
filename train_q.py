import numpy as np
from board import Board
from randomplayer import RandomPlayer
from greedyplayer import GreedyPlayer
from minimaxplayer import MMPlayer
from qplayer import QPlayer
from player import Player


def main():
    board = Board()

#    game = Game(board)
    lr = 0.03
    disc = 0.9
    eps = 0.3

    p1 = QPlayer('P1', lr, disc, eps)
    p2 = RandomPlayer('P2')

    p1.verbose = False

    resettrain = input('Reset training? (y/n)')
    cyctrain = input('Cycles to train?')
    board.train = True
    if resettrain == 'n':
        p1.Q = np.genfromtxt('Qfile.txt', delimiter = ',')
    else:
        random.seed(1)
        print('TRAINING against RANDOM...')
        wins = 0
        ties = 0
        for trial in range(100000):
            board.resetBoard()
            board.displayBoard()
            board.train = True
            if (trial % 2) == 1: # P2 goes first every other trial
                board.set_player(1)
            done = board.check_done()
            while not done:
                player = board.get_player()
                if player == 0:
                    pit = p1.get_move(board)
                else:
                    pit = p2.get_move(board)
                board.move(pit)
                done = board.check_done()
            if (board.pits[7] < board.pits[0]):
                wins += 1
                p1.rewards[-1] += 25
            elif (board.pits[7] == board.pits[0]):
                ties += 1
                p1.rewards[-1] += 10
            p1.rewards[-1] += (board.pits[0] - board.pits[7]) # reward for win/tie/loss
            p1.updateQ2(p1.states.copy(), p1.actions.copy(), p1.rewards.copy())
            p1.resetStates()
            p1.resetActions()
            p1.resetRewards()
            if (trial+1) % 1000 == 0:
                print('wins/1000:', wins, 'ties:', ties)
                wins = 0
                ties = 0

        print('TRAINING against Greedy...')
        p2 = RandomPlayer('P2')
        wins = 0
        ties = 0
        for trial in range(100000):
            board.resetBoard()
            board.displayBoard()
            board.train = True
            if (trial % 2) == 1: # P2 goes first every other trial
                board.set_player(1)
            done = board.check_done()
            while not done:
                player = board.get_player()
                if player == 0:
                    pit = p1.get_move(board)
                else:
                    pit = p2.get_move(board)
                board.move(pit)
                done = board.check_done()
            if (board.pits[7] < board.pits[0]):
                wins += 1
                p1.rewards[-1] += 25
            elif (board.pits[7] == board.pits[0]):
                ties += 1
                p1.rewards[-1] += 10
            p1.rewards[-1] += (board.pits[0] - board.pits[7]) # reward for win/tie/loss
            p1.updateQ2(p1.states.copy(), p1.actions.copy(), p1.rewards.copy())
            p1.resetStates()
            p1.resetActions()
            p1.resetRewards()
            if (trial+1) % 1000 == 0:
                print('wins/1000:', wins, 'ties:', ties)
                wins = 0
                ties = 0

    print('TRAINING against Minimax...')
    p1.seteps(0.02)
    p2 = MMPlayer('P2')
    wins=0
    ties=0
    for trial in range(int(cyctrain)):
        board.resetBoard()
        if (trial % 2) == 1: # P2 goes first every other trial
            board.set_player(1)
        done = board.check_done()
        while not done:
            player = board.get_player()
            if player == 0:
                pit = p1.get_move(board)
            else:
                pit = p2.get_move(board)
            board.move(pit)
            done = board.check_done()
        if (board.pits[7] < board.pits[0]):
            wins += 1
            p1.rewards[-1] += 25
        elif (board.pits[7] == board.pits[0]):
            ties += 1
            p1.rewards[-1] += 10
        p1.rewards[-1] += (board.pits[0] - board.pits[7]) # reward for win/tie/loss
        p1.updateQ2(p1.states.copy(), p1.actions.copy(), p1.rewards.copy())
        #print('actions:', p1.actions)
        p1.resetStates()
        p1.resetActions()
        p1.resetRewards()
        if (trial+1) % 1000 == 0:
            print('wins/1000:', wins, 'ties:', ties)
            wins = 0
            ties = 0
            #print(np.array_str(p1.Q[1], precision=2))

    np.savetxt('Qfile.txt', p1.Q, delimiter=',')
    

if __name__ == '__main__':
    main()
