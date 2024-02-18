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
        else:
            self.revealCell(row, col)

        if self.checkFull():
            print("You win!")
            self.playing = False
            self.won = True

def zeroCells (playerBoard):
    zero_cells = []
    for i in range(len(playerBoard)):
        for j in range(len(playerBoard[i])):
            if playerBoard[i][j] == 0:
                zero_cells.append((i, j))
    return zero_cells

def adjacentToBorderCells(board, n):
    zero_cells = zeroCells(board)
    aobc = []
    for cell in zero_cells:
        for adj in adjacentCells(cell[0],cell[1]):
            if inBounds(adj[0], adj[1], n):
                aobc.append(adj)
    return aobc

def adjacentCells(x, y):
    return [
        (x, y + 1),
        (x, y - 1),
        (x + 1, y),
        (x - 1, y),
        (x + 1, y + 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x - 1, y - 1)
    ]

def inBounds(row, col, n):
    if row < 0 or row >= n or col < 0 or col >= n:
        return False
    return True

def returnPlayerBoard(self):
    return self.playerBoard

def printPlayerBoard(self):
    for i in range(len(self.playerBoard)):
        print(self.playerBoard[i])

def printBoard(self):
    for i in range(len(self.board)):
        print(self.board[i])

def printCustomBoard(board):
    for i in range(len(board)):
        print(board[i])