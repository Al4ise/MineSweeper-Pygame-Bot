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

def zeroCells (board):
    zero_cells = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 'b':
                zero_cells.append((i, j))
    return zero_cells

def adjacentToBorderCells(self, board):
    zero_cells = zeroCells(board)
    aobc = []
    for cell in zero_cells:
        for adj in adjacentCells(cell[0],cell[1]):
            if inBounds(self, adj[0], adj[1]):
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
        (x - 1, y - 1),
    ]

def inBounds(self, row, col):
    if row < 0 or row >= self.n or col < 0 or col >= self.n:
        return False
    return True

def returnPlayerBoard(self):
    return self.playerBoard