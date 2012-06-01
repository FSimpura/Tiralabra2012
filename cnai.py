#   Artificial intelligence for "connect n"
#   Written by Frans Simpura

import sys

# The AI for "connect n"

class cnai:

    # Initialize the AI with target depth
    def __init__(self, skillLevel):
        self.skillLevel = max (skillLevel, 0)
    
    # Calculates the final value for the heuristics
    def tokenCountWeighted(self, n):
        if n == 0:
            return 0
        return pow(2, (n-1)*2)
        
    # Sums up all the heuristics of given move
    def moveTotalValue(self, move, board):
        return self.decDiagonalValue(move, board) + self.incDiagonalValue(move, board) + self.horizontalValue(move, board) + self.verticalValue(move, board) 

    # Calculates the diagonal (increasing) heuristics of given move
    def incDiagonalValue(self, move, board):
        heuristics = 0
        tokenCount = 0
        for offset in range(-board.toWin+1, 1): # Define the offset according to the win condition
            for step in range(board.toWin):
                if not board.inBounds(move.x + offset + step, move.y + offset + step):
                    tokenCount = 0
                    break # Out-of-bounds; winning condition will not be met
                if board.getBoard()[move.x + offset + step][move.y + offset + step] == move.token:
                   tokenCount += 1
                elif board.getBoard()[move.x + offset + step][move.y + offset + step] != None:
                    tokenCount = 0
                    break
            heuristics += self.tokenCountWeighted(tokenCount)
            tokenCount = 0
        return heuristics
        
    # Calculates the diagonal (decreasing) heuristics of given move
    def decDiagonalValue(self, move, board):
        heuristics = 0
        tokenCount = 0
        for offset in range(-board.toWin+1, 1): # Define the offset according to the win condition
            for step in range(board.toWin):
                if not board.inBounds(move.x - offset - step, move.y + offset + step):
                    tokenCount = 0
                    break # Out-of-bounds; winning condition will not be met
                if board.getBoard()[move.x - offset - step][move.y + offset + step] == move.token:
                   tokenCount += 1
                elif board.getBoard()[move.x - offset - step][move.y + offset + step] != None:
                    tokenCount = 0
                    break
            heuristics += self.tokenCountWeighted(tokenCount)
            tokenCount = 0
        return heuristics
        
    # Calculates the vertical heuristics of given move
    def verticalValue(self, move, board):
        heuristics = 0
        tokenCount = 0
        for offset in range(-board.toWin+1, 1): # Define the offset according to the win condition
            for step in range(board.toWin):
                if not board.inBounds(move.x + offset + step, move.y):
                    break # Out-of-bounds; winning condition will not be met
                if board.getBoard()[move.x + offset + step][move.y] == move.token:
                   tokenCount += 1
                elif board.getBoard()[move.x + offset + step][move.y] != None:
                    tokenCount = 0
                    break
            heuristics += self.tokenCountWeighted(tokenCount)
            tokenCount = 0
        return heuristics
        
    # Calculates the horizontal heuristics of given move   
    def horizontalValue(self, move, board):
        heuristics = tokenCount = 0
        for offset in range(-board.toWin+1, 1): # Define the offset according to the win condition
            for step in range(board.toWin):
                if not board.inBounds(move.x, move.y + offset + step):
                    tokenCount = 0
                    break # Out-of-bounds; winning condition will not be met
                if board.getBoard()[move.x][move.y + offset + step] == move.token:
                    tokenCount += 1
                elif board.getBoard()[move.x][move.y + offset + step] != None:
                    tokenCount = 0
                    break
            heuristics += self.tokenCountWeighted(tokenCount)
            tokenCount = 0
        return heuristics
	
    # Determines the best move according to the heuristics of the possible moves
    def bestMove(self, token, board):
        depth = self.skillLevel
        best = -sys.maxint - 1
        bestMove = None
        for n in range(board.width): # generate a list of the possible moves
            newMove = board.dropToken(token, n, True)
            if newMove != None:
                latest = self.minimax(newMove, depth, board.copyBoard())
                if board.isWinningMove(newMove):
                    return newMove
                if latest > best:
                    best = latest
                    bestMove = newMove
        return bestMove
    
    # Calculates the best move according to the skillLevel using minimax algorithm	
    def minimax(self, move, depth, board):
        board.dropToken(move.token, move.y)
        if board.isWinningMove(move):
            return sys.maxint

        if depth == 0:
            return self.moveTotalValue(move, board)

        alpha = sys.maxint
        enemyToken = None
        enemyMoves = []
        if move.token == "X":
            enemyToken = "O"
        else:
            enemyToken = "X"  
        for n in range(board.width): # generate a list of all the possible enemy moves
            newMove = board.dropToken(enemyToken, n, True)
            if newMove != None:
                enemyMoves.append(newMove)
        for enemyMove in enemyMoves:
            alpha = min(alpha, -(self.minimax(enemyMove, depth-1, board.copyBoard())))

        return alpha
        
# A wrap for the coordinates and the token of a move        
class Move:
    
    def __init__(self, x, y, token):
        self.x = x
        self.y = y
        self.token = token
    
    # Return x, y and token information for debugging
    def __repr__(self):
        return "[(" + str(self.x) + ", " + str(self.y)+ "), " + str(self.token) + "]"
       
# A coordinate pair (x, y)
class Coords:

    def __init__(self, x, y):
        self.x = x
        self.y = y
		
	# Increases positive coordinates and decreases negative coordinates by one; passes on zeroes.
    # Used in the row checkers
    def inc(self):
        if self.x < 0:
            self.x -= 1
        if self.x > 0:
            self.x += 1
        if self.y > 0:
            self.y += 1
        if self.y < 0:
            self.y -= 1
	
# A representation of a board of size x*y
class Board:
    # Initialize an empty board of given size x*y
    def __init__(self, columns, rows, toWin):
        self.width = max (2, columns) # Min value of 2
        self.height = max (2, rows) # Min value of 2
        self.LAST_COLUMN = self.width-1
        self.LAST_ROW = self.height-1
        self.board = [[None for i in range(self.width)] for j in range(self.height)]
        self.toWin = max (2, toWin) # Tokens in a row required for winning, min value of 2
        self.playerToken = "O"
        self.enemyToken = "X"
        self.tokenCount = 0
	
    # Returns a copy of self
    def copyBoard(self):
        newBoard = Board(self.width, self.height, self.toWin)
        newBoardMatrix = [[None for i in range(self.width)] for j in range(self.height)]
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                newBoardMatrix[row][column] = self.board[row][column]
        newBoard.setBoard(newBoardMatrix)
        return newBoard
        
    # Returns the reference of the internal board
    def getBoard(self):
        return self.board
    
    # Changes the internal board reference
    def setBoard(self, board):
        self.board = board
    
    # Returns True if the board is full, otherwise False
    def isFull(self):
        return self.tokenCount == (self.width * self.height)
    
    # Places the given token at the bottommost free row of the given column. Return True if succees, otherwise False.
    def dropToken(self, token, column, test = False):
        if self.inBounds(0, column):
            for row in range(len(self.board)):
                if self.board[row][column] == None:
                    if not test:
                        self.board[row][column] = token
                        self.tokenCount += 1
                    return Move(row, column, token)
        return None
	
    # Returns True if the column at given coordinate is full, otherwise False
    def isFullColumn(self, c):
        return self.board[self.LAST_ROW][c] != None
    
    # Returns True if a given token at given coordinates forms a winning row vertically, horizontally or diagonally, otherwise False
    def isWinningMove(self, move):
        coords = [Coords(1, 0), Coords(0, 1), Coords(1, 1), Coords(1, -1)]
        i = 0
        x = move.x
        y = move.y
        token = move.token
        while i <= 3:
            doLeft = doRight = True
            rowCounter = 1
            d = coords[i]
            i += 1
            while doLeft or doRight:
                if doLeft and self.inBounds(x+d.x, y+d.y) and self.getToken(x+d.x, y+d.y) == token:
                    rowCounter += 1
                    if rowCounter == self.toWin:
                        return True
                else:
                    doLeft = False
                if doRight and self.inBounds(x-d.x, y-d.y) and self.getToken(x-d.x, y-d.y) == token:
                    rowCounter += 1
                    if rowCounter == self.toWin:
                        return True
                else:
                    doRight = False
                d.inc()
        return False
	
    # Calls dropToken and checks if that move wins 
    def dropAndCheck(self, token, column):
        move = self.dropToken(token, column)
        if isinstance(move, Move):
            return self.isWinningMove(move)
        return False	
		
    # Returns True if given coordinates are within the board, otherwise False.
    def inBounds(self, x, y):
        return x <= self.LAST_ROW and x >= 0 and y <= self.LAST_COLUMN and y >= 0
		
    # Returns the token in the cell at given coordinates
    def getToken(self, x, y):
        if self.inBounds(x, y):
            return self.board[x][y]
        return None
        
# Basic board printing, for testing
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

# Plays a token (X) at given column and lets AI make its move
def playAgainstAI(n):
    if n < board.width:
        if not board.isFullColumn(n):
            if board.dropAndCheck("X", n):
                return 1
            if board.dropAndCheck("O", ai.bestMove("O", board).y):
                return 2
    return 0

# A continuous play mode with user input; drops a token at given column number.
def play():
        while True:
            c = raw_input("> ")
            try:
                w = playAgainstAI(int(c))
                printAsBoard(board)
                if w == 1:
                    print "X wins!"
                    break
                if w == 2:
                    print "O wins!"
                    break

                if board.isFull():
                    print "Draw!"
                    break
            except ValueError:
                pass

# Not to be run when imported            
if __name__ == "__main__":                
    if (len(sys.argv) > 4):
        d = int(sys.argv[1])
        w = int(sys.argv[2])
        h = int(sys.argv[3])
        toWin = int(sys.argv[4])
        board = Board(w, h, toWin)
        ai = cnai(d)
        printAsBoard(board)
        try:
            play()
        except KeyboardInterrupt:
            print("\n Interrupted!")
            sys.exit()         