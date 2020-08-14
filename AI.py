from tetramino import *
from validMove import *
import copy as cp

class AI:

    def __init__(self, holesFactor, linesFactor, heightFactor):
        self.holesFactor = holesFactor
        self.linesFactor = linesFactor
        self.heightFactor = heightFactor
        self.move = None

    def moveCalculator(self, activePiece, pieces):

        validMoves = []

        piece = tetramino(activePiece.win, tetramino.shapes.index(activePiece.setup))
        piece.x = 50
        piece.y = 25
        piece.generator()

        i = 0
        while i <= 3:
            prevX = 0
            while not piece.x == prevX:
                while piece.isActive:
                    piece.move(pieces)
                piece.isActive = True
                validMoves.append(validMove(
                    piece.x, piece.y, i, piece, pieces, self.holesFactor, self.linesFactor, self.heightFactor))
                prevX = piece.x
                piece.y = 25
                piece.generator()
                piece.right(pieces)
            piece.rotate()
            flag = True
            c = 0
            while flag:
                piece.left(pieces)
                c += 1
                if c > 20:
                    break
                for tetra in piece.tetras:
                    if tetra.x == 50:
                        flag = False
            piece.isActive = True
            i += 1

        maxScore = -100
        for move in validMoves:
            maxScore = move.score if move.score > maxScore else maxScore

        for move in validMoves:
            if move.score == maxScore:
                self.move = move

    def applyMove(self, activePiece, pieces):
        if not self.move == None:
            while self.move.nRotation > 0:
                activePiece.rotate()
                self.move.nRotation -= 1
            activePiece.x = self.move.x
            activePiece.generator()
            while activePiece.isActive:
                activePiece.move(pieces)
