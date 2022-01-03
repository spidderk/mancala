
class Player:

    def __init__(self, pid):
        self.pid = pid
        if self.pid == 'P1':
            self.valid_pits = [1,2,3,4,5,6]
            self.invalid_pits = [8,9,10,11,12,13]
        else:
            self.valid_pits = [8,9,10,11,12,13]
            self.invalid_pits = [1,2,3,4,5,6]

#    def move(self, pit, board):
#        stones = int(board.pits[pit])
#        board.pits[pit] = 0
#        index = pit
#        for i in range(1,stones+1):
#            index = (index - 1) % 14
#            if (self.pid == 'P1') and (index == 7):
#                #print('wrap p1')
#                index = 6
#            elif (self.pid == 'P2') and (index == 0):
#                #print('wrap p2')
#                index = 13
#            board.pits[index] = board.pits[index] + 1
#
#            
#        if board.pits[index] == 1:
#            # ended on an empty pit
#            if self.pid == 'P1' and index in [1,2,3,4,5,6]:
#                board.pits[0] += (board.pits[14-index]+1)
#                board.pits[14-index] = 0
#                board.pits[index] = 0
#            if self.pid == 'P2' and index in [8,9,10,11,12,13]:
#                board.pits[7] += (board.pits[14-index]+1)
#                board.pits[14-index] = 0
#                board.pits[index] = 0
#
#        board.displayBoard()
#        return ((self.pid == 'P1' and index == 0) or (self.pid == 'P2' and index == 7))
#            
#            
