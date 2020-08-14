import pygame as pg
from rect import *
from tetramino import *
from validMove import *
import random as rm
import copy as cp
#import pudb
#pu.db

class tetris:
    
    winX = 1050
    winY = 1050
    pg.init()
    pg.key.set_repeat(100, 50)
    clock = pg.time.Clock()
    size = 50

    T_shape = [[1, 1, 1],
            [0, 1, 0],
            [0, 0, 0]]
    I_shape = [[0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    Z_shape = [[1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]]
    O_shape = [[1, 1],
            [1, 1]]
    S_shape = [[0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]]
    L_shape = [[0, 1, 0],
            [0, 1, 0],
            [1, 1, 0]]
    J_shape = [[0, 1, 0],
            [0, 1, 0],
            [0, 1, 1]]
    shapes = [T_shape, L_shape, J_shape, S_shape, Z_shape, O_shape, I_shape]

    colors = [(255, 0, 255), (255, 100, 100), (0, 0, 255),
            (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 150)]


    overlay = [rect(win, 50, 25, winY-50, (0, 0, 0)),
            rect(win, 600, 100, 200, (0, 0, 0))]
    overlay[0].width = 500
    
    font = pg.font.Font('freesansbold.ttf', 32)

    def __init__(self):
        self.win = pg.display.set_mode((winX, winY))
        self.totalPoints = 0
        self.activePiece = tetramino(win, size, shapes[buff], colors[buff])
        self.run = True
        self.pieces = []
        prev = 0
        buff = rm.randrange(0, 6)
        counter = 0
    def reset(self):
        self.pieces = []
        totalPoints = 0
        self.run = True

    def moveCalculator(self,holesFactor,linesFactor,heightFactor):

        piece = tetramino(self.activePiece.win, self.activePiece.width,
                        cp.deepcopy(self.activePiece.setup), self.activePiece.color)
        validMoves = []

        piece.x = 50
        piece.y = 25
        piece.generator()

        i = 0
        while i <= 3:
            prevX = 0
            while not piece.x == prevX:
                while piece.isActive:
                    piece.move(self.pieces)
                piece.isActive = True
                validMoves.append(validMove(piece.x, piece.y, i, piece, self.pieces,holesFactor,linesFactor,heightFactor))
                prevX = piece.x
                piece.y = 25
                piece.generator()
                piece.right(self.pieces)
            piece.rotate()
            flag = True
            c = 0
            while flag:
                piece.left(self.pieces)
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
                return move

    def applyMove(self,move):

        if not move == None:
            while move.nRotation > 0:
                self.activePiece.rotate()
                move.nRotation -= 1
            self.activePiece.x = move.x
            self.activePiece.generator()
            while self.activePiece.isActive:
                self.activePiece.move(self.pieces)
                #draw()

    def main(self,holesFactor,linesFactor,heightFactor,auto):
        self.activePiece = tetramino(win, size, shapes[buff], colors[buff])
        buff = rm.randrange(0, 7)

        prev = tetramino(win, size, shapes[buff], colors[buff])
        prev.x = overlay[1].x + (overlay[1].width-(size*len(shapes[buff][0])))//2
        prev.y = overlay[1].y + (overlay[1].height-(size*len(shapes[buff][0])))//2
        prev.generator()

        while not self.activePiece == 0:
            counter += 1
            if not len(self.pieces) == 0:
                cleanCheck(self.pieces)
            k = 0
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.run = False
                        self.run = False
                    if (event.key == pg.K_r):
                        self.activePiece.rotate()
                    if event.key == pg.K_LEFT:
                        self.activePiece.left(self.pieces)
                    if event.key == pg.K_RIGHT:
                        self.activePiece.right(self.pieces)
                    if event.key == pg.K_DOWN:
                        self.activePiece.move(self.pieces)
            if (counter % 100) == 0:
                self.activePiece.move(self.pieces)
            if auto:
                applyMove(moveCalculator(holesFactor,linesFactor,heightFactor))
            else:
                draw()
                #clock.tick(1000)
            for piece in self.pieces:
                if piece.y <= 25:
                    self.run = False
            if not self.activePiece.isActive:
                for tetra in self.activePiece.tetras:
                    tetra.isActive = False
                    self.pieces.append(tetra)
                self.activePiece = 0


    def cleanCheck(self,self.pieces):
        global totalPoints
        grid = []
        rows = []
        points = 0

        for piece in self.pieces:
            grid.append(piece.y)

        Y = 25
        while Y <= winY:
            rows.append([Y, 0])
            Y += 50

        for item in grid:
            for row in rows:
                if item == row[0]:
                    row[1] += 1

        for row in rows:
            if row[1] == 10:
                for piece in self.pieces:
                    if piece.y == row[0]:
                        piece.marked = 70
                    if piece.y < row[0]:
                        piece.marked += 1
                points += 1

        if points == 1:
            points = 40
        elif points == 2:
            points = 100
        elif points == 3:
            points = 300
        elif points == 4:
            points = 1200
        totalPoints += points

        i = 0
        while i < len(self.pieces):
            if not self.pieces[i].marked == 0 and self.pieces[i].marked < 70:
                while self.pieces[i].marked > 0:
                    self.pieces[i].y += size
                    self.pieces[i].marked -= 1

            elif self.pieces[i].marked >= 70:
                self.pieces.pop(i)

            else:
                i += 1

        return self.pieces

    def draw(self,):
        for over in overlay:
            over.draw()

        prev.draw()

        for piece in self.pieces:
            piece.draw()

        self.activePiece.draw()

        text = font.render('Points: ' + str(totalPoints),
                        True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.x, textRect.y = (600, 350)
        win.blit(text, textRect)
        pg.display.update()

        pg.display.flip()
        win.fill((20, 20, 20))

    def game(self,holesFactor,linesFactor,heightFactor):
        while self.run:
            main(holesFactor,linesFactor,heightFactor,True)
        return totalPoints

if __name__ == '__main__':
    main(1,1,1,False)
        
