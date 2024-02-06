from Logic import *
from MineSweeper import Minesweeper


class Bot(Minesweeper):
    def __init__(self, n, b):
        self.boardKnowledge = [[Sentence() for _ in range(n)] for _ in range(n)]

    def evalBoard(self, playerBoard):
        for i in range(len(playerBoard)):
            for j in range(len(playerBoard[i])):
                if playerBoard[i][j] == "b":
                    self.boardKnowledge[i][j] = self.evalCell(i, j, playerBoard)

    def evalCell(self, i, j, playerBoard):
        adjacentValidMoves = self.adjacentValidMoves(playerBoard, i, j)
        possibleBombLocations = Or()

        for loc in adjacentValidMoves:
            possibleBombLocations.add(loc)

        adjacentInvalidMoves = self.adjacentInvalidMoves(playerBoard, i, j)
        impossibleBombLocations = And()

        for loc in adjacentInvalidMoves:
            impossibleBombLocations.add(loc)

        cellKnowledge = And(possibleBombLocations, Not(impossibleBombLocations))
        return cellKnowledge

    def adjacentValidMoves(self, playerBoard, x, y):
        adjacents = self.adjacentCells(x, y)
        validMoves = []
        for i in adjacents:
            if self.inBounds(i[0], i[1]) and playerBoard[i[0]][i[1]] == 0:
                validMoves.append(i)
        return validMoves

    def adjacentInvalidMoves(self, playerBoard, x, y):
        adjacents = self.adjacentCells(x, y)
        invalidMoves = []
        for i in adjacents:
            if playerBoard[i[0]][i[1]] != 0:
                invalidMoves.append(i)
        return invalidMoves

    def placeFlag(self, board):
        return (0, 0)

    def clickCell(self, board):
        return (0, 0)
