import random
class Minesweeper:
    def __init__(self, n):  # nxn grid
        self.playing = True
        # contains bombs and numbers
        cell_content_options = [1, 2, 3, 4, 5, 6] # 6 is bomb
        self.board = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                self.board[i][j] = random.choice(cell_content_options)

        # contains flags and uncovered numbers
        self.playerBoard = [[0] * n for _ in range(n)]
        ...

    def printPlayerBoard(self):
        for i in range(len(self.playerBoard)):
            print(self.playerBoard[i])
    
    def printBoard(self):
        for i in range(len(self.board)):
            print(self.board[i])
    
    def placeSymbol(self, row, col, PLACEFLAG):
        if PLACEFLAG == True:
            if self.playerBoard[row][col] == 7:
                # Remove Flag
                self.playerBoard[row][col] = 0
            else:
                # Place Flag
                self.playerBoard[row][col] = 7
        elif PLACEFLAG == False:
            # Place Bomb
            if self.board[row][col] == 6:
                print("You lose!")
                self.playing = False
                self.won = False
            else:
                self.playerBoard[row][col] = self.board[row][col]

            if self.checkFull():
                print("You win!")
                self.playing = False
                self.won = True
        
    def didWin(self):
        return self.won
    
    def checkFull(self): # True if full, false if not
        for i in range(len(self.playerBoard)):
            for j in range(len(self.playerBoard[i])):
                if self.playerBoard[i][j] == 0 or self.playerBoard[i][j] == 7:
                    return False
        return True
