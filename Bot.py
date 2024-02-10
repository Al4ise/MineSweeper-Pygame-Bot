from Logic import *
import sharedMethods as s

class Bot():
    def __init__(self, playerBoard):
        self.n = len(playerBoard)
        self.playerBoard = playerBoard
        self.bombBoardKnowledge = [[Sentence() for _ in range(self.n)] for _ in range(self.n)]
        self.cleanBoardKnowledge = [[Sentence() for _ in range(self.n)] for _ in range(self.n)]

    def evalBoard(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                self.evalCell(i, j, board)

    def evalCell(self, i, j, board):
        self.bombBoardKnowledge[i][j] = self.bombKnowledge(i, j, board)
        self.cleanBoardKnowledge[i][j] = self.cleanKnowledge(i, j, board)
    
    def logicallyPlaceFlag (self):
        cell = self.bestMove(self.bombBoardKnowledge)
        if cell:
            s.placeSymbol(self, cell[0], cell[1], True)
        else:
            return False
        return True

    def logicallyUncover (self):
        cell = self.bestMove(self.cleanBoardKnowledge)
        if cell:
            s.placeSymbol(self, cell[0], cell[1], True)
        else:
            return False
        return True


    def bombKnowledge (self, i, j, board):
        adjacentValidMoves = self.adjacentValidMoves(board, i, j)
        possibleBombLocations = Or()

        for loc in adjacentValidMoves:
            sym = Symbol(self.symbolName(loc))
            possibleBombLocations.add(sym) # bomb is on one of these places # ... for other than 1
        
        certainBombLocations = And()
        for i in adjacentValidMoves:
            if i == 'f':
                sym=Symbol(self.symbolName(i))
                certainBombLocations.add(i)
        
        adjacentInvalidMoves = self.adjacentInvalidMoves(board, i, j)
        impossibleBombLocations = And() # bomb is not in any of these places

        for loc in adjacentInvalidMoves:
            sym = Symbol(self.symbolName(loc))
            impossibleBombLocations.add(sym)

        cellKnowledge = And(possibleBombLocations, Not(impossibleBombLocations), certainBombLocations)
        return cellKnowledge   
    
    def cleanKnowledge (self, i, j, board):
        adjacentValidMoves = self.adjacentValidMoves(board, i, j)
        possibleCleanLocations = Or()
        ...

        certainCleanLocations = And()
        if board[i][j] == 1:
            for cell in adjacentValidMoves:
                sym = Symbol(self.symbolName(cell))
                certainCleanLocations.add(sym)

        impossibleCleanLocations = And()
        ...

        cellKnowledge = And(possibleCleanLocations, Not(impossibleCleanLocations), certainCleanLocations)
        return cellKnowledge

    def bestMove (self, knowledgeBoard):
        border_cells = s.adjacentToBorderCells(self, self.playerBoard)
        for cell in border_cells:
            self.dropCellNum(cell[0], cell[1])
            # concat knowledge, first only from one cell, then from it and its adjacents with an adjustable max depth
            all_knowledge = self.concatCellKnowledge(knowledgeBoard, cell[0], cell[1])
            for adj in s.adjacentCells(cell[0], cell[1]):
                query = self.symbolName(adj)
                if model_check(all_knowledge, query):
                    return cell # coordinates

        return None

    def dropCellNum (self, x, y):
        adj = s.adjacentCells(x, y)
        for i, j in adj:
            if self.playerBoard[i][j] == 'f':
                self.playerBoard[x][y] -= 1
        
    def symbolName (self, coordinates):
        coordinates = (0, 0)
        return f'{coordinates[0]}, {coordinates[1]}'

    def concatCellKnowledge (self, knowledgeBoard, center_x, center_y, concat=And(), depth=0):
        if depth > 1:
            return concat
        else:
            concat.add(knowledgeBoard[center_x][center_y])
            for i, j in s.adjacentCells(center_x, center_y):
                self.evalCell(i, j, knowledgeBoard)
                concat.add(knowledgeBoard[i][j])

                self.concatCellKnowledge(knowledgeBoard, i, j, concat, depth+1)

    def adjacentValidMoves(self, board, x, y):
        adjacents = s.adjacentCells(x, y)
        validMoves = []
        for i in adjacents:
            if s.inBounds(self, i[0], i[1]) and board[i[0]][i[1]] == 0:
                validMoves.append(i)
        return validMoves

    def adjacentInvalidMoves(self, board, x, y):
        adjacents = s.adjacentCells(x, y)
        invalidMoves = []
        for i in adjacents:
            if board[i[0]][i[1]] != 0:
                invalidMoves.append(i)
        return invalidMoves

    def placeFlag(self, board):
        return (0, 0)

    def clickCell(self, board):
        return (0, 0)
