#   Artificial intelligence for "connect n"
#   Written by Frans Simpura 

# TODO: The AI
class cnai:
	
    def _init__(self, skillLevel):
        self.skillLevel = skillLevel
		
    # TODO: Calculates the best move according to the skillLevel using minimax algorithm	
    def makeMove(self, token, board):
        pass

# A coordinate pair (x, y)
class Coords:

    def __init__(self, x, y):
        self.x = x
        self.y = y
		
	# Increases positive coordinates and decreases negative coordinates by one; passes on zeroes.	
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
    def __init__(self, columns, rows):
        self.width = columns
        self.height = rows
        self.LAST_COLUMN = columns-1
        self.LAST_ROW = rows-1
        self.board = [[None for i in range(self.width)] for j in range(self.height)]
        self.toWin = 4 # Tokens in a row required for winning
	
    # Return the reference of the board
    def getBoard(self):
        return self.board
		
    # Places the given token at the bottommost free row of the given column. Return True if succees, otherwise False.
    def dropToken(self, token, column):
        if self.inBounds(0, column):
            for row in range(len(self.board)):
                if self.board[row][column] == None:
                    self.board[row][column] = token
                    return Coords(row, column)
        return None
	
    # Returns True if a given token at given coordinates forms a winning row vertically, horizontally or diagonally, otherwise False
    def isWinningMove(self, x, y):
        coords = [Coords(1, 0), Coords(0, 1), Coords(1, 1), Coords(1, -1)]
        i = 0
        token = self.getToken(x, y)
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
        coords = self.dropToken(token, column)
        if isinstance(coords, Coords):
            return self.isWinningMove(coords.x, coords.y)
        return False		
		
    # Returns True if given coordinates are within the board, otherwise False.
    def inBounds(self, x, y):
        return x <= self.LAST_ROW and x >= 0 and y <= self.LAST_COLUMN and y >= 0
		
    # Returns the token in the cell at given coordinates
    def getToken(self, x, y):
        if self.inBounds(x, y):
            return self.board[x][y]
        return None