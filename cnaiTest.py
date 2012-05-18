from cnai import Board
import unittest
 
# TODO: Unittests for Board and cnai
class cnaiTest(unittest.TestCase):
    
    # Set up a blank board of size 10x15.
    def setUp(self):
        self.board = Board(10, 15)
    
    # Makes sure the board fills completely
    def test_fillBoard(self):
        for i in range(10):
            for j in range(15):
                self.board.dropToken("O", i)
        for x in self.board.getBoard():
           self.assertEqual(None in x, False)
     
    # TODO: ???
    def test_dropToken(self):
        for i in range(20):
            for j in range(30):
                self.board.dropToken("O", i)
 
    # Once the board is filled with O's, makes sure every cell counts as a winning move
    def test_filled_IsWinning(self):
        for i in range(10):
            for j in range(15):
                self.board.dropToken("O", i)
        for i in range(10):
            for j in range(15):
                self.assertEqual(self.board.isWinningMove(j, i), True)
 
def printAsBoard(board):
    for row in range(board.LAST_ROW, -1, -1):
        for column in range(0, board.LAST_COLUMN+1):
            cell = board.getBoard()[row][column]
            if cell == None:
                print ("."),
            else:
                print(cell),
        print("")
    print("")
	
unittest.main()