import numpy as np

class Board:

    def __init__(self, numpits = 6, numseeds = 4):
        self.train = True
        self.player = 0
        self.numpits = numpits
        self.numseeds = numseeds
        self.pits = np.zeros(2*numpits+2, dtype=int)
        self.p0pits = []
        self.p1pits = []
        for i in range(1,numpits+1):
            self.pits[i] = numseeds
            self.p0pits.append(i)
            self.pits[i+numpits+1] = numseeds
            self.p1pits.append(i+numpits+1)
        self.homes = {0:0, 1:numpits+1}
            
    def resetBoard(self):
        self.__init__()
        
    def score(self):
        return [self.pits[self.homes[0]], self.pits[self.homes[1]]]
        
    def copy(self):
        board = Board(self.numpits, self.numseeds)
        board.set_pits(self.pits)
        board.set_player(self.player)

        return board

    def set_pits(self, pits):
        self.pits = np.copy(pits)
        
    def get_pits(self):
        return self.pits
    
    def displayBoard(self):
        if self.train == False:
            print('   0    1    2    3    4    5    6    7')
            print('-----------------------------------------')
            print('|    |    |    |    |    |    |    |    |')
            print('|    ',end='')
            for i in range(1,7):
                print(f'| {int(self.pits[i]):2d} ', end='')
            print('|    |')
            print(f'| {int(self.pits[0]):2d} ',end='')
            print('|-----------------------------|', end='')
            print(f' {int(self.pits[7]):2d} |')
            print('|    |    |    |    |    |    |    |    |')
            print('|    ',end='')
            for i in range(6):
                print(f'| {int(self.pits[13-i]):2d} ', end='')
            print('|    |')
            print('-----------------------------------------')
            print('   0   13   12   11   10    9    8    7')
        return
       
    def check_done(self):
        p1sum = np.sum(self.pits[1:self.numpits+1])
        p2sum = np.sum(self.pits[self.numpits+2:2*self.numpits+2])
        if p1sum == 0:
            self.pits[self.homes[1]] += p2sum
            self.pits[self.numpits+2:2*self.numpits+2] *= 0
            return True
        elif p2sum == 0:
            self.pits[self.homes[0]] += p1sum
            self.pits[1:self.numpits+1] *= 0
            return True
        return False
        
    def move(self, pit):
        seeds = self.pits[pit] # number of seeds to sow
        if seeds == 0: # empty pit, illegal move
            #print("illegal pit:", pit)
            #self.displayBoard()
            return False
        self.pits[pit] = 0 # set current pit empty
        other = 1 - self.player
        index = pit
        for i in range(1,seeds+1):
            index = (index - 1) % (2*self.numpits+2)
            if index == self.homes[other]:
                index = (index - 1) % (2*self.numpits+2)
            self.pits[index] = self.pits[index] + 1

            
        if self.pits[index] == 1: # ended on an empty pit
            if self.player == 0 and index in self.p0pits:
                self.pits[self.homes[0]] += (self.pits[2*self.numpits+2-index]+1)
                self.pits[2*self.numpits+2-index] = 0
                self.pits[index] = 0
            if self.player == 1 and index in self.p1pits:
                self.pits[self.homes[1]] += (self.pits[2*self.numpits+2-index]+1)
                self.pits[2*self.numpits+2-index] = 0
                self.pits[index] = 0
                
        if index != self.homes[self.player]: # did not end on player's home
            self.player = 1 - self.player # switch player
            
        #done = self.check_done() # check if either side is empty and update

        self.displayBoard()
        return True
        
    def get_player(self):
        return self.player

    def set_player(self, player):
        self.player = player
        
    def allowed_moves(self):
        allowed_moves = []
        if self.player == 0:
            valid_pits = self.p0pits
        else:
            valid_pits = self.p1pits
        for pit in valid_pits:
            if self.pits[pit] > 0:
                allowed_moves.append(pit)
        return allowed_moves

