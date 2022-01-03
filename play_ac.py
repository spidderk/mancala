from board import Board
from humanplayer import HumanPlayer
from actorcritic import ActorCriticPlayer
from actorcritic import ActorCriticModel

import torch

def main():
    board = Board()
    bins = 6
    neurons = 256
    #model = ActorCriticModel(bins*2+2, bins, neurons)
    model = torch.load('./results/final_model.pt')
    model.eval()

    p1 = ActorCriticPlayer('P1', model)
    #torch.load('./results/final_model.pt')
    p2 = HumanPlayer('P2')
    #p1.verbose = True

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
