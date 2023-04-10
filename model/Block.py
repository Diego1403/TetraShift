class Block:
    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)

    def getPos(self):
        return Block(self.x, self.y)

    def GoRight(self):
        self.x = self.x + 1

    # converts x to int
    def getX(self):
        return int(self.x)

    def getY(self):
        return int(self.y)

    def GoLeft(self):
        self.x = self.x - 1

    def GoDown(self):
        self.y = self.y + 0.1

    def __str__(self):
        rep = "(" + str(self.x) + " , " + str(self.y) + ")"
        return rep
