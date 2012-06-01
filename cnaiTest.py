from cnai import cnai, Board, Move
import unittest
 
# TODO: Unittests for Board and cnai
class cnaiTest(unittest.TestCase):
    
    # Set up a blank board of size 10x15.
    def setUp(self):
        self.board = Board(10, 15, 4)
    
    # Makes sure the board fills completely
    def test_fillBoard(self):
        for i in range(10):
            for j in range(15):
                self.board.dropToken("O", i)
        for x in self.board.getBoard():
           self.assertEqual(None in x, False)
            
    # Once the board is filled with O's, makes sure every cell counts as a winning move
    def test_filled_IsWinning(self):
        for i in range(10):
            for j in range(15):
                self.board.dropToken("O", i)
        for i in range(10):
            for j in range(15):
                move = Move(j, i, "O")
                self.assertEqual(self.board.isWinningMove(move), True)
    
    def test_isWinning(self):
        for n in range(10):
            self.board = Board(10, 15, 4)
            self.board.dropToken("X", n)
            self.board.dropToken("X", n)
            self.board.dropToken("X", n)
            move = self.board.dropToken("X", n)
            self.assertEqual(self.board.isWinningMove(move), True)
        for n in range(7):
            self.board = Board(10, 15, 4)
            self.board.dropToken("X", 0+n)
            self.board.dropToken("X", 1+n)
            self.board.dropToken("X", 2+n)
            move = self.board.dropToken("X", 3+n)
            self.assertEqual(self.board.isWinningMove(move), True)
        for n in range(7):
            self.board = Board(10, 15, 4)
            self.board.dropToken("X", 0+n)
            self.board.dropToken("O", 1+n)
            self.board.dropToken("X", 1+n)
            self.board.dropToken("O", 2+n)
            self.board.dropToken("O", 2+n)
            self.board.dropToken("X", 2+n)
            self.board.dropToken("O", 3+n)
            self.board.dropToken("O", 3+n)
            self.board.dropToken("O", 3+n)
            move = self.board.dropToken("X", 3+n)
            self.assertEqual(self.board.isWinningMove(move), True)
    
    # Makes sure symmetrical heuristic values are equal
    def test_heuristicsCheckCorrect(self):
        ai = cnai(0)
        for n in range(10):
            self.board = Board(10, 15, 4)
            self.board.dropToken("X", 0+n)
            self.board.dropToken("X", 0+n)
            self.board.dropToken("X", 1+n)
            self.board.dropToken("X", 9-n)
            self.board.dropToken("X", 9-n)
            self.board.dropToken("X", 8-n)
            for i in range(5):
                a = Move(3, 1+i, "X")
                b = Move(3, 8-i, "X")
                self.assertEqual(ai.moveTotalValue(a, self.board), ai.moveTotalValue(b, self.board))
    
    # Win AI 0 by playing aggressively
    def test_aiLosesDepthZero(self):
        ai = cnai(0)
        self.board.dropToken("X", 1)
        self.board.dropToken("O", ai.bestMove("O", self.board).y)
        self.board.dropToken("X", 1)
        self.board.dropToken("O", ai.bestMove("O", self.board).y)
        self.board.dropToken("X", 1)
        self.board.dropToken("O", ai.bestMove("O", self.board).y)
        self.assertEqual(self.board.dropAndCheck("X", 1), True)

    # Lets AI 0 win by playing badly
    def test_aiWinsDepthZero(self):
        ai = cnai(0)
        self.board.dropToken("X", 9)
        self.board.dropToken("O", ai.bestMove("O", self.board).y)
        self.board.dropToken("X", 9)
        self.board.dropToken("O", ai.bestMove("O", self.board).y)
        self.board.dropToken("X", 9)
        self.board.dropToken("O", ai.bestMove("O", self.board).y)
        self.assertEqual(self.board.dropAndCheck("O", ai.bestMove("O", self.board).y), True)

    # Tests if AI (any) picks the best spot to win
    def test_aiPicksWinning(self):
        for n in range(4):
            self.board = Board(10, 15, 4)
            ai = cnai(0+n)
            self.board.dropToken("X", 9)
            self.board.dropToken("X", 9)
            self.board.dropToken("X", 9)
            self.board.dropToken("O", 0+n)
            self.board.dropToken("O", 1+n)
            self.board.dropToken("O", 3+n)
            self.assertEqual(ai.bestMove("O", self.board).y, 2+n)
            
    # Tests if AI (> 0) denies player's win
    def test_aiDeniesPlayer(self):
        for n in range(3):
            self.board = Board(10, 15, 4)
            ai = cnai(1+n)
            self.board.dropToken("O", 9)
            self.board.dropToken("O", 9)
            self.board.dropToken("X", 0+n)
            self.board.dropToken("X", 1+n)
            self.board.dropToken("X", 3+n)
            self.assertEqual(ai.bestMove("O", self.board).y, 2+n)
	
unittest.main()