import random
from Logic import *
import random

class Minesweeper:
    def __init__(self, n, percentBombs, setBoard=None):  # nxn grid, b% bombs
        self.playing = True

        # contains flags and uncovered numbers
        self.playerBoard = [[0] * n for _ in range(n)]

        # contains bombs and numbers
        if setBoard:
            self.board = setBoard
            self.n = len(setBoard)
            self.percentBombs = None
        else:
            self.n = n
            self.percentBombs = percentBombs
            self.board = self.generateRandBoard(n, percentBombs)
            #self.playerBoard=self.revealLongestWhitePath()

    def adjacentCells(self, x, y):
        return [
            (x, y + 1),
            (x, y - 1),
            (x + 1, y),
            (x - 1, y),
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y - 1),
        ]

    def generateRandBoard(self, n, percentBombs):
        board = [[0] * n for _ in range(n)]

        # place bombs at n random places
        cells = [(i, j) for i in range(n) for j in range(n)]
        bombCount = n * n * percentBombs // 100

        random_cells = random.sample(cells, bombCount)
        for cell in random_cells:
            board[cell[0]][cell[1]] = "b"

        # pick one cell at random which is not a bomb
        board = self.evaluateBoard(board)

        return board
    

    def generateSolvableguraBoard(self, first_x, first_y): 
        board = self.generateRandBoard(self.n, self.percentBombs)
        if board[first_x][first_y] == 'b':
            random_cell=self.pick_random_clean_cell(board)
            if random_cell: 
                board[random_cell[0]][random_cell[1]] = 'b'
                board[first_x][first_y] = 0
        
        solved = False
        while not solved:
            board = self.cleanBoard(board)
            board = self.evaluateBoard(board)
            board = self.solveByDeduction(board)
            ...
            solved = self.checkFull(board)
            if solved:
                solved=True
            else:
                # get adjacents of last revealed cells 
                adj = self.adjacentBombsToBorderCells(board)
                rand_adj = random.choice(adj) if adj else None
                # swap one with a random 0
                random_zero=self.pick_random_clean_cell(board)
                if random_zero: 
                    board[random_zero[0]][random_zero[1]] = 'b'
                    board[first_x][first_y] = 0
        return None

    def checkSolvability (self, board):
        ...

    def adjustSolvability (self, board):
        ...

    def cleanBoard (self, board):
        b = board
        for i in range(len(b)):
            for j in range(len(b[i])):
                if b[i][j] != 'b' and b[i][j] != 0:
                    b[i][j] = 0
        return b

    def evaluateBoard (self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != "b":
                    cellnumber = 0
                    # look at the surroundings of that cell and count the number of bombs
                    cellnumber = self.defCellNumber(i, j, board)

                    # place that number in the cell
                    board[i][j] = cellnumber

        return board
        
    def adjacentsToBorderCells(self, board):
        zero_cells = self.zeroCells(board)
        aobc = []
        for cell in zero_cells:
            for adj in self.adjacentCells(cell[0],cell[1]):
                if self.inBounds(adj[0], adj[1]):
                    aobc.append(adj)
        return aobc
    
    def adjacentBombsToBorderCells (self, board):
        aobc = self.adjacentsToBorderCells(board)
        abz = []
        for i in aobc:
            if i == 'b':
                abz.append(i)
        return abz

    def pick_random_clean_cell(self, board):
        zero_cells = self.zeroCells(board)
        if zero_cells:
            random_cell = random.choice(zero_cells)
            return random_cell
        return

    def zeroCells (self, board):
        zero_cells = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != 'b':
                    zero_cells.append((i, j))
        return zero_cells
    
    def inBounds(self, row, col):
        if row < 0 or row >= self.n or col < 0 or col >= self.n:
            return False
        return True

    def incrementCellNumber(self, row, col, board): 
        if self.inBounds(row, col) and board[row][col] == "b":
            return 1
        return 0

    def defCellNumber(self, row, col, board):
        adjacents = [
            (row, col + 1),
            (row, col - 1),
            (row + 1, col),
            (row - 1, col),
            (row + 1, col + 1),
            (row + 1, col - 1),
            (row - 1, col + 1),
            (row - 1, col - 1),
        ]
        cellnumber = 0
        for i in adjacents:
            cellnumber += int(self.incrementCellNumber(i[0], i[1], board))
        return cellnumber

    def printPlayerBoard(self):
        for i in range(len(self.playerBoard)):
            print(self.playerBoard[i])

    def printBoard(self):
        for i in range(len(self.board)):
            print(self.board[i])

    def returnPlayerBoard(self):
        return self.board

    def placeSymbol(self, row, col, PLACEFLAG):
        if PLACEFLAG == True:
            if self.playerBoard[row][col] == "f":
                # Remove Flag
                self.playerBoard[row][col] = 0
            else:
                # Place Flag
                self.playerBoard[row][col] = "f"
        elif PLACEFLAG == False:
            # Place Bomb
            if self.board[row][col] == "b":
                print("You lose!")
                self.playing = False
                self.won = False
            elif self.board[row][col] == 0:
                self.revealCell(row, col)
                self.revealWhite(row, col)
            else:
                self.revealCell(row, col)

            if self.checkFull():
                print("You win!")
                self.playing = False
                self.won = True

    def revealWhite(self, row, col, depth=0, explored=set()):
        # if the cell is empty, reveal all adjacent cells
        if self.board[row][col] == 0:
            self.revealAdjacents(row, col)
            explored.add((row, col))
            emptyAdjCells = self.emptyAdjCells(row, col)
            for i, j in emptyAdjCells:
                if not (i, j) in explored:
                    self.revealWhite(i, j, depth + 1, explored)
        else:
            return depth
            
    def emptyAdjCells(self, row, col):
        adjCells = self.adjacentCells(row, col)
        eac = []
        for i, j in adjCells:
            if self.inBounds(i, j):
                if self.board[i][j] == 0:
                    eac.append((i, j))
        return eac

    def revealCell(self, row, col):
        if self.board[row][col] == 0:
            self.playerBoard[row][col] = 'e'
        else:
            self.playerBoard[row][col] = self.board[row][col]

    def revealAdjacents(self, row, col):
        for i, j in self.adjacentCells(row, col):
            if self.inBounds(i, j):
                self.revealCell(i, j)

    def didWin(self):
        return self.won

    def checkFull(self, board=None):  # True if full, false if not
        if not board: board=self.playerBoard
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    return False
        return True
