from Logic import *
from MineSweeper import Minesweeper

class Bot(Minesweeper):
    def __init__(self, n, b):
        self.bombBoardKnowledge = [[Sentence() for _ in range(n)] for _ in range(n)]
        self.cleanBoardKnowledge = [[Sentence() for _ in range(n)] for _ in range(n)]


    def evalBoard(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                self.evalCell(i, j, board)

    def evalCell(self, i, j, board):
        self.bombBoardKnowledge[i][j] = self.bombKnowledge(i, j, board)
        self.cleanBoardKnowledge[i][j] = self.cleanKnowledge(i, j, board)
    
    def logicallyPlaceFlag (self):
        self.bestMove(self.bombBoardKnowledge)
        self.placeSymbol()

    def logicallyUncover (self):
        self.bestMove(self.cleanBoardKnowledge)
        ...

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
        #adjacentBombs = self.adjacentFlag
        ...
     
    def bestMove (self, knowledgeBoard):
        border_cells = self.adjacentsToBorderCells(knowledgeBoard)
        for cell in border_cells:
            # concat knowledge, first only from one cell, then from it and its adjacents with an adjustable max depth
            all_knowledge = self.concatCellKnowledge(knowledgeBoard, cell[0], cell[1])
            for adj in self.adjacentCells(cell[0], cell[1]):
                query = self.symbolName(adj)
                if model_check(all_knowledge, query):
                    return cell # coordinates
        
        return None

    def symbolName (self, coordinates):
        coordinates = (0, 0)
        return f'{coordinates[0]}, {coordinates[1]}'

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
