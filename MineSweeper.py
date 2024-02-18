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
    
    def throwBombElsewhere (self, x, y, board):
        random_cell=self.pick_random_clean_cell(board)
        if random_cell: 
            board[random_cell[0]][random_cell[1]] = 'b'
            board[x][y] = 0
        return board
    
    def generateSolvableaBoard(self, first_x, first_y): 
        _playerBoard = [[0] * self.n for _ in range(self.n)]
        board = self.generateRandBoard(self.n, self.percentBombs)

        if board[first_x][first_y] == 'b':
            board = self.throwBombElsewhere(first_x, first_y, board)
            _playerBoard = self.revealAdjacents(first_x, first_y, _playerBoard, board)
            s.printCustomBoard(_playerBoard)
        
        _playerBoard = self.revealCell(first_x, first_y, _playerBoard, board)

        adjbombs = self.adjacentBombsToBorderCells(_playerBoard)
        ...
        while adjbombs:
            print(adjbombs)

            for i, j in adjbombs:
                adjandself = s.adjacentCells(i, j)
                adjandself.append((i, j))
                for x, y in adjandself:
                    if board[x][y] == 'b':
                        board = self.throwBombElsewhere(x, y, board)
                        _playerBoard = self.revealAdjacents(x, y, _playerBoard, board)
                        

        
        #_playerBoard = self.revealCell(first_x, first_y, _playerBoard, board)
        solved = False

        while not solved:
            #board = self.cleanBoard(board)
            board = self.defineBoard(board)
            s.printCustomBoard(_playerBoard)
            print(self.adjacentBombsToBorderCells(_playerBoard))

            board = self.solveByDeduction(_playerBoard)
            

            solved = self.checkFull(board)
            if solved:
                solved=True
            else:
                # get adjacents of last revealed cells 
                adj = self.adjacentBombsToBorderCells(board)
                x_rand_adj, y_rand_adj = random.choice(adj)               
                # swap one with a random 0
                random_zero=self.pick_random_clean_cell(board)
                if random_zero: 
                    board[random_zero[0]][random_zero[1]] = 'b'
                    board[x_rand_adj][y_rand_adj] = 0
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
                
            s.printPlayerBoard(bot)

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
        aobc = s.adjacentToBorderCells(board, self.n)
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
        if s.inBounds(row, col, self.n) and board[row][col] == "b":
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

    def revealWhite(self, row, col, board, playerBoard, depth=0, explored=set()):
        def _revealCell(row, col, playerBoard, board):
            pb = playerBoard
            if board[row][col] == 0:
                pb[row][col] = 'e'
                
            else:
                pb[row][col] = board[row][col]
            
            return pb

        def _revealAdjacents(row, col, playerBoard, board):
            pb = playerBoard
            for i, j in s.adjacentCells(row, col):
                if s.inBounds(i, j, self.n):
                    pb = _revealCell(i, j, playerBoard, board)
            
            return pb
        
        # if the cell is empty, reveal all adjacent cells
        if board[row][col] == 0:
            pb = _revealAdjacents(row, col, playerBoard, board)
            explored.add((row, col))
            emptyAdjCells = self.emptyAdjCells(row, col, board)
            for i, j in emptyAdjCells:
                if not (i, j) in explored:
                    self.revealWhite(i, j, board, pb, depth + 1, explored)
        else:
            return playerBoard

    def emptyAdjCells(self, row, col, board):
        adjCells = s.adjacentCells(row, col)
        eac = []
        for i, j in adjCells:
            if s.inBounds(i, j, self.n):
                if board[i][j] == 0:
                    eac.append((i, j))
        return eac

    def revealCell (self, row, col, playerBoard, board):
        pb = playerBoard
        if board[row][col] == 0:
            pb = self.revealWhite(row, col, board, pb)
            
        else:
            pb[row][col] = board[row][col]
        
        return pb

    def revealAdjacents(self, row, col, playerBoard, board):
        pb = playerBoard
        for i, j in s.adjacentCells(row, col):
            if s.inBounds(i, j, self.n):
                pb = self.revealCell(i, j, pb, board)
        
        return pb

    
    def didWin(self):
        return self.won

    def checkFull(self, board=None):  # True if full, false if not
        if not board: board=self.playerBoard
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    return False
        return True
