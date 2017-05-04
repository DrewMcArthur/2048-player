"""
    Drew McArthur
    Classes to play 2048.
    Includes piece and board class.  use apply to make a move
"""

import random
import math

class Piece:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val

    def __lt__(self, other):
        return self.val < other.val

    def __str__(self):
        return "_" if self.isEmpty() else str(self.val)
    
    def isEmpty(self):
        return self.val == 0
    
    def empty(self):
        self.val = 0
    
    def doubleValue(self):
        self.val *= 2

class Board:
    def __init__(self, orig=None):
        if not orig:
            self.pieces = [[Piece(0) for c in range(4)] 
                                           for r in range(4)]
            self.score = 0
            self.width = 2
            self.addRandomPiece()
            self.addRandomPiece()
        else:
            self.pieces = [[Piece(orig.pieces[r][c].val) for c in range(4)] 
                                                         for r in range(4)]
            self.score = orig.score
            self.width = orig.width

    def __eq__(self, other):
        for r in range(4):
            for c in range(4):
                if not self.pieces[r][c] == other.pieces[r][c]:
                    return False
        return True
    
    def gameover(self):
        return self.getEmptyLocations() == [] and self.getOps() == []

    def printBoard(self):
        print("printed with width",self.width)
        for row in self.pieces:
            [print(str(piece).rjust(self.width), end="") for piece in row]
            print()

    def getOps(self):
        ops = ["left", "right", "up", "down"]
        ret = []
        for op in ops:
            if self.apply(op) != self:
                ret.append(op)
        return ret

    def checkWidth(self, p):
        n = math.floor(math.log(p.val))
        self.width = n if n > self.width

    def getEmptyLocations(self):
        """ returns a list of (r, c) tuples referring to empty locations 
            in the board. """
        ret = []
        for r in range(len(self.pieces)):
            for c in range(len(self.pieces[r])):
                if self.pieces[r][c].isEmpty():
                    ret.append((r, c))

        return ret

    def addRandomPiece(self):
        r, c = random.choice(self.getEmptyLocations())
        v = random.choice([2,2,2,4])
        self.pieces[r][c] = Piece(v)

    def apply(self, op):
        """ slide all the pieces in the board in the direction of [op]. 
            double duplicates, and add a new random piece at an empty location. 
        """
        new = Board(self)

        if op == "left":
            new.slideLeft()
        elif op == "right":
            new.slideRight()
        elif op == "up":
            new.slideUp()
        elif op == "down":
            new.slideDown()
        else:
            print("Error: Unrecognized Op:", op)
            return None

        if new != self:
            new.addRandomPiece()

        return new

    def slideDown(self):
        # rotate clockwise
        self.pieces = list(list(x) for x in zip(*self.pieces[::-1]))
        self.slideLeft()
        # rotate counterclockwise
        self.pieces = list(list(x) for x in zip(*self.pieces))[::-1]

    def slideUp(self):
        # rotate clockwise
        self.pieces = list(list(x) for x in zip(*self.pieces[::-1]))
        self.slideRight()
        # rotate counterclockwise
        self.pieces = list(list(x) for x in zip(*self.pieces))[::-1]

    def slideRight(self):
        # rotate clockwise
        self.pieces = list(list(x) for x in zip(*self.pieces[::-1]))
        self.pieces = list(list(x) for x in zip(*self.pieces[::-1]))
        self.slideLeft()
        # rotate counterclockwise
        self.pieces = list(list(x) for x in zip(*self.pieces))[::-1]
        self.pieces = list(list(x) for x in zip(*self.pieces))[::-1]
        """
        # for each row,
        for r in range(4):
            # merge duplicate pieces in the right direction
            for c in range(3, 0, -1):
                if not self.pieces[r][c].isEmpty():
                    i=1
                    if c-i > 0 and self.pieces[r][c-i].isEmpty():
                        i+=1
                    if self.pieces[r][c] == self.pieces[r][c-i]:
                        self.pieces[r][c].doubleValue()
                        self.score += self.pieces[r][c].val
                        self.pieces[r][c-i].empty()

            # slide all the pieces right
            for c in range(3, 0, -1):
                i = 0
                while self.pieces[r][c].isEmpty() and i < 4:
                    self.pieces[r] = ([Piece(self, 0)] +
                                      self.pieces[r][:c] + 
                                      self.pieces[r][c+1:])
                    i += 1
        """

    def slideLeft(self):
        # for each row
        for r in range(4):
            # merge pieces
            for c in range(3):
                if not self.pieces[r][c].isEmpty():
                    i=1
                    while c+i < 3 and self.pieces[r][c+i].isEmpty():
                        i+=1
                    if self.pieces[r][c] == self.pieces[r][c+i]:
                        self.pieces[r][c].doubleValue()
                        self.checkWidth(self.pieces[r][c])
                        self.score += self.pieces[r][c].val
                        self.pieces[r][c+i].empty()

            # slide all the pieces left
            for c in range(3):
                i = 0
                while self.pieces[r][c].isEmpty() and i < 4:
                    self.pieces[r] = (self.pieces[r][:c] + 
                                      self.pieces[r][c+1:] + 
                                      [Piece(0)])
                    i += 1

