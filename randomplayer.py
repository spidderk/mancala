import random
from player import Player

class RandomPlayer(Player):

    def get_move(self, board):
        done = False
        #print(self.pid, "turn (Random)")
        while not(done):
            pit = random.randint(self.valid_pits[0],self.valid_pits[5])
            if board.pits[pit] != 0 and pit in self.valid_pits:
                done = True
        return pit
