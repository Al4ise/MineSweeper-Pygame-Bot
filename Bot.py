from Logic import *
import sharedMethods as s

class Bot():
    def __init__(self, playerBoard):
        self.n = len(playerBoard)
        self.playerBoard = playerBoard
        self.bombBoardKnowledge = [[Sentence() for _ in range(self.n)] for _ in range(self.n)]
        self.cleanBoardKnowledge = [[Sentence() for _ in range(self.n)] for _ in range(self.n)]
        self.checked = []

    def evalBoard(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                self.evalCell(i, j, board)

    def evalCell(self, i, j, board):
        var = self.bombKnowledge(i, j, board)
        if isinstance(var, Sentence):
            self.bombBoardKnowledge[i][j] = var
        #self.cleanBoardKnowledge[i][j] = self.cleanKnowledge(i, j, board)
    
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
        adjacentValidMoves = self.adjacentValidMoves(self.playerBoard, i, j)

        possibleBombLocations = Or()
        cellKnowledge = And()

        for loc in adjacentValidMoves:
            sym = Symbol(self.symbolName(loc))
            possibleBombLocations.add(sym) # bomb is on one of these places # ... for other than 1
        
        certainBombLocations = And()
        for p in adjacentValidMoves:
            if p == 'f':
                sym=Symbol(self.symbolName(p))
                certainBombLocations.add(p)
        
        adjacentInvalidMoves = self.adjacentInvalidMoves(self.playerBoard, i, j)
        impossibleBombLocations = And() # bomb is not in any of these places

        for loc in adjacentValidMoves:
            if board[loc[0]][loc[1]] != 0:
                sym = Symbol(self.symbolName(loc))
                possibleBombLocations.add(sym)  
            
        for loc in adjacentInvalidMoves:
            if board[loc[0]][loc[1]] != 0:
                sym = Symbol(self.symbolName(loc))
                impossibleBombLocations.add(sym)

        try:
            tmp = possibleBombLocations.symbols()
            cellKnowledge.add(possibleBombLocations)
        except:
            pass

        try:
            tmp = certainBombLocations.symbols()
            cellKnowledge.add(certainBombLocations)
        except:
            pass

        try:
            tmp = impossibleBombLocations.symbols()
            cellKnowledge.add(Not(impossibleBombLocations))
        except:
            pass

        try:
            tmp = cellKnowledge.symbols()
            return cellKnowledge  
        except:
            return None
    
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
                name = self.symbolName(adj)
                if name not in self.checked:
                    query = Symbol(name)
                    self.checked.append(name)
                    if model_check(all_knowledge, query):
                        return cell  # coordinates
        return None

    def dropCellNum (self, x, y):
        adj = s.adjacentCells(x, y)
        try: 
            num = int(self.playerBoard[x][y])
        except:
            return self.playerBoard[x][y]
        
        for i, j in adj:
            if self.playerBoard[i][j] == 'f':
                self.playerBoard[x][y] = str(num-1)
        
    def symbolName (self, coordinates):
        return f'{coordinates[0]}, {coordinates[1]}'

    def concatCellKnowledge (self, knowledgeBoard, center_x, center_y, concat=And(), depth=0):
        if depth > 1:
            return concat
        else:
            c = knowledgeBoard[center_x][center_y]
            if isinstance(c, Sentence):
                concat.add(knowledgeBoard[center_x][center_y])
            
            for i, j in s.adjacentCells(center_x, center_y):
                if isinstance(c, Sentence):
                    self.evalCell(i, j, knowledgeBoard)
                    concat.add(knowledgeBoard[i][j])
            
            return concat
            #self.concatCellKnowledge(knowledgeBoard, i, j, concat, depth+1) 
        ...

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
