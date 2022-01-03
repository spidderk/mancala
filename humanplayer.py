from player import Player

class HumanPlayer(Player):

#    def turn(self, board):
#        turnNotDone = True
#        print(self.pid, "turn (Human)")
#        while turnNotDone and not(board.check_done()):
#            pit_str = input("pick a pit: ")
#            try:
#                pit = int(pit_str)
#            except:
#                pit = 0
#            if board.pits[pit] != 0 and pit in self.valid_pits:
#                turnNotDone = self.move(pit, board)
#            else:
#                print("Must pick a non-empty pit from: ", self.valid_pits)
                
    def get_move(self, board):
        done = False
        print(self.pid, "turn (Human)")
        while not(done):
            pit_str = input("pick a pit: ")
            try:
                pit = int(pit_str)
            except:
                pit = 0
            if board.pits[pit] != 0 and pit in self.valid_pits:
                done = True
            else:
                print("Must pick a non-empty pit from: ", self.valid_pits)
        return pit
