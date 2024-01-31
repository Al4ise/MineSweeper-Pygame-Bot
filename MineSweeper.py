class Minesweeper:
    def __init__(self, n):  # nxn grid
        # contains bombs and numbers
        self.board = [[0] * n] * n

        # contains flags and uncovered numbers
        self.playerBoard = [[0] * n] * n

        ...

    def placeFlag(self, pos): ...

    def evaluateSpace(self, pos): ...
