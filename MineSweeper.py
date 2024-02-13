import random
from Logic import *
import sharedMethods as s
from Bot import Bot
import random

class Minesweeper:
    def __init__(self, n, percentBombs, first_x=None, first_y=None, setBoard=None):  # nxn grid, b% bombs
        self.playing = True
        self.won = False

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
            if not(first_x and first_y):
                self.board = self.generateRandBoard(n, percentBombs)
            else:
                self.board = self.generateSolvableaBoard(first_x, first_y)

    def generateRandBoard(self, n, percentBombs):
        board = [[0] * n for _ in range(n)]

        # place bombs at n random places
        cells = [(i, j) for i in range(n) for j in range(n)]
        bombCount = n * n * percentBombs // 100

        random_cells = random.sample(cells, bombCount)
        for cell in random_cells:
            board[cell[0]][cell[1]] = "b"

        # pick one cell at random which is not a bomb
        board = self.defineBoard(board)

        return board
    

    def generateSolvableaBoard(self, first_x, first_y): 
        board = self.generateRandBoard(self.n, self.percentBombs)
        if board[first_x][first_y] == 'b':
            random_cell=self.pick_random_clean_cell(board)
            if random_cell: 
                board[random_cell[0]][random_cell[1]] = 'b'
                board[first_x][first_y] = 0
        
        solved = False

        while not solved:
            board = self.cleanBoard(board)
            board = self.defineBoard(board)
            board = self.solveByDeduction(board)
            solved = self.checkFull(board)
            if solved:
                solved=True
            else:
                # get adjacents of last revealed cells 
                adj = self.adjacentBombsToBorderCells(board)
                # swap one with a random 0
                random_zero=self.pick_random_clean_cell(board)
                if random_zero: 
                    board[random_zero[0]][random_zero[1]] = 'b'
                    board[first_x][first_y] = 0
        return board

    def checkSolvability (self, board):
        ...

    def adjustSolvability (self, board):
        ...

    def solveByDeduction (self, bot):
        bot=Bot(self.playerBoard)

        success = True

        while success == True or self.checkFull(s.returnPlayerBoard(bot)):
            success = False
            if bot.logicallyPlaceFlag():
                success = True
            else:
                print("No certain Bombs")
                
            s.prinPlayerBoard(bot)

            if bot.logicallyUncover():
                #success = True
                ...
            else:
                print("No certain Cleans")
        return s.returnPlayerBoard(self)

    def cleanBoard (self, board):
        b = board
        for i in range(len(b)):
            for j in range(len(b[i])):
                if b[i][j] != 'b' and b[i][j] != 0:
                    b[i][j] = 0
        return b

    def defineBoard (self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != "b":
                    cellnumber = 0
                    # look at the surroundings of that cell and count the number of bombs
                    cellnumber = self.defCellNumber(i, j, board)

                    # place that number in the cell
                    board[i][j] = cellnumber

        return board
    
    def adjacentBombsToBorderCells (self, board):
        aobc = s.adjacentToBorderCells(self, board)
        abz = []
        for i in aobc:
            if i == 'b':
                abz.append(i)
        return abz

    def pick_random_clean_cell(self, board):
        zero_cells = s.zeroCells(board)
        if zero_cells:
            random_cell = random.choice(zero_cells)
            return random_cell
        return

    def incrementCellNumber(self, row, col, board): 
        if s.inBounds(self, row, col) and board[row][col] == "b":
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

    def printBoard(self):
        for i in range(len(self.board)):
            print(self.board[i])

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
        adjCells = s.adjacentCells(row, col)
        eac = []
        for i, j in adjCells:
            if s.inBounds(self, i, j):
                if self.board[i][j] == 0:
                    eac.append((i, j))
        return eac

    def revealCell(self, row, col):
        if self.board[row][col] == 0:
            self.playerBoard[row][col] = 'e'
        else:
            self.playerBoard[row][col] = self.board[row][col]

    def revealAdjacents(self, row, col):
        for i, j in s.adjacentCells(row, col):
            if s.inBounds(self, i, j):
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
