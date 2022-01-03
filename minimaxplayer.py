import sys
import random
from player import Player

class MMPlayer(Player):
    """
    Minimax agent with alpha-beta pruning for mancala.
    """

    max_depth = 4

    first_round = True
    player = 0

    def __init__(self, pid, seed=34, depth=4):
        Player.__init__(self, pid)
        #random.seed(seed)
        #self.random = random.random()
        self.max_depth = depth

    def minimax(self, player, depth, board, pit, alpha, beta):
        if depth == 0:
            return board.score()[player]

        test_board = board.copy()
        #test_board.train = False
#        print('before move', pit, 'depth', depth)
#        test_board.displayBoard()
        test_board.move(pit)
#        print('after move', pit, 'depth', depth)
#        test_board.displayBoard()

        maxi = (test_board.get_player() == player)

        move_options = test_board.allowed_moves()
        best_move = -sys.maxsize if maxi else sys.maxsize

        for move_slot in move_options:
            current_value = self.minimax(
                player, depth - 1, test_board, move_slot, alpha, beta)

            if maxi:
                best_move = max(current_value, best_move)
                alpha = max(alpha, best_move)
            else:
                best_move = min(current_value, best_move)
                beta = min(beta, best_move)

            if beta <= alpha:
                return best_move

        return best_move

    def get_move(self, board):
        #print(self.pid, "turn (MM)")
        # Determine which player we are
        if self.first_round:
            self.player = board.get_player()
            print('MMPlayer:', self.player)
            self.first_round = False

        # If there is only one valid move, return that move
        allowed_moves = board.allowed_moves()
        #print('allowed moves:', allowed_moves)
        if len(allowed_moves) == 1:
            return allowed_moves[0]

        moves_and_scores = []
        for move in board.allowed_moves():
            minimax_score = self.minimax(
                self.player, self.max_depth, board, move, -sys.maxsize, sys.maxsize)
            #print('move:', move, 'score:', minimax_score)
            moves_and_scores.append([move, minimax_score])

        scores = [item[1] for item in moves_and_scores]
        max_score = max(scores)

        potential_moves = []
        for move_and_score in moves_and_scores:
            if move_and_score[1] == max_score:
                potential_moves.append(move_and_score[0])
        #print('potential moves:', potential_moves)
        return random.choice(potential_moves)

