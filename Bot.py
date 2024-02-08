from Logic import *
from MineSweeper import Minesweeper


class Bot(Minesweeper):
    def __init__(self, n, b):
        self.boardKnowledge = [[Sentence() for _ in range(n)] for _ in range(n)]

    def evalBoard(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == "b":
                    self.boardKnowledge[i][j] = self.evalCell(i, j, board)

    def evalCell(self, i, j, board):
        adjacentValidMoves = self.adjacentValidMoves(board, i, j)
        possibleBombLocations = Or()

        for loc in adjacentValidMoves:
            possibleBombLocations.add(loc)

        adjacentInvalidMoves = self.adjacentInvalidMoves(board, i, j)
        impossibleBombLocations = And()

        for loc in adjacentInvalidMoves:
            impossibleBombLocations.add(loc)

        cellKnowledge = And(possibleBombLocations, Not(impossibleBombLocations))
        return cellKnowledge

    def bestMove (self, board):
        border_cells = self.adjacentsToBorderCells(board)
        for cell in border_cells:
            # concat knowledge, first only from one cell, then from it and its adjacents with an adjustable max depth
            all_knowledge = self.concatCellKnowledge(board, cell[0], cell[1])
            for adj in self.adjacentCells(cell[0], cell[1]):
                model_check(all_knowledge, )
                if True:
                    # return cell
                    ...
        ...


    def concatCellKnowledge (self, board, center_x, center_y, concat=And(), depth=0):
        if depth > 1:
            return concat
        else:
            for i in self.adjacentCells(center_x, center_y):
                concat.add(self.evalCell(i[0], i[1], board))
                concat.add(self.concatCellKnowledge(board, i[0], i[1], concat, depth+1))

    def adjacentValidMoves(self, board, x, y):
        adjacents = self.adjacentCells(x, y)
        validMoves = []
        for i in adjacents:
            if self.inBounds(i[0], i[1]) and board[i[0]][i[1]] == 0:
                validMoves.append(i)
        return validMoves

    def adjacentInvalidMoves(self, board, x, y):
        adjacents = self.adjacentCells(x, y)
        invalidMoves = []
        for i in adjacents:
            if board[i[0]][i[1]] != 0:
                invalidMoves.append(i)
        return invalidMoves

    def placeFlag(self, board):
        return (0, 0)

    def clickCell(self, board):
        return (0, 0)
