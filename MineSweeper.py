import random
from Logic import *


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
            self.board = self.generateBoard(n, percentBombs)
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

    def generateBoard(self, n, percentBombs):
        board = [[0] * n for _ in range(n)]

        # place bombs at n random places
        cells = [(i, j) for i in range(n) for j in range(n)]
        bombCount = n * n * percentBombs // 100

        random_cells = random.sample(cells, bombCount)
        for cell in random_cells:
            board[cell[0]][cell[1]] = "b"

        # pick one cell at random which is not a bomb
        for i in range(n):
            for j in range(n):
                if board[i][j] != "b":
                    cellnumber = 0
                    # look at the surroundings of that cell and count the number of bombs
                    cellnumber = self.defCellNumber(i, j, board)

                    # place that number in the cell
                    board[i][j] = cellnumber

        return board

    def revealLongestWhitePath(self): # horrendous code
        # for each blank
        maxpath = 0
        board = self.playerBoard
        # do revealwhite
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    testGame = Minesweeper(self.n, self.percentBombs, self.board)
                    score = testGame.revealWhite(i, j)
                    print(score)
                    if score is not None and maxpath is not None and score > maxpath:
                        maxpath = score
                        board = testGame.returnPlayerBoard()

            self.playerBoard = board
            ...

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

        self.printPlayerBoard()

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
            self.playerBoard[row][col] = "e"
        else:
            self.playerBoard[row][col] = self.board[row][col]

    def revealAdjacents(self, row, col):
        for i, j in self.adjacentCells(row, col):
            if self.inBounds(i, j):
                self.revealCell(i, j)

    def didWin(self):
        return self.won

    def checkFull(self):  # True if full, false if not
        for i in range(len(self.playerBoard)):
            for j in range(len(self.playerBoard[i])):
                if self.playerBoard[i][j] == 0:
                    return False
        return True
