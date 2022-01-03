import numpy as np
from board import Board
from qplayer import QPlayer
from humanplayer import HumanPlayer
from player import Player


def main():
    board = Board()

    lr = 0.03
    disc = 0.9
    eps = 0.3

    p1 = QPlayer('P1', lr, disc, eps)
    p1.Q = np.genfromtxt('Qfile.txt', delimiter = ',')
    p1.train = False
    p1.seteps(0.0)
    p1.verbose = True
    p2 = HumanPlayer('P2')

    print('*** GAME 1: AI plays first ***')
    board.resetBoard()
    board.train = False
    board.displayBoard()
    done = board.check_done()
    while not done:
        player = board.get_player()
        if player == 0:
            pit = p1.get_move(board)
        else:
            pit = p2.get_move(board)
        board.move(pit)
        done = board.check_done()

    [scorep1g1, scorep2g1] = board.score()
    board.displayBoard()
    print('Game1 score: ', scorep1g1, scorep2g1)

    print('*** GAME 2: AI plays second ***')
    board.resetBoard()
    p1.resetStates()
    p1.resetActions()
    p1.resetRewards()

    board.train = False
    board.displayBoard()
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

    [scorep1g2, scorep2g2] = board.score()
    print('Game2 score: ', scorep1g2, scorep2g2)
    print('Total score: ', scorep1g1+scorep1g2, scorep2g1+scorep2g2)

if __name__ == '__main__':
    main()
