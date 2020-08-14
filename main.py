import pygame as pg
from rect import *
from tetramino import *
from validMove import *
import random as rm
import copy as cp
#import pudb
#pu.db

def reset():
    global pieces
    global totalPoints
    global run

    pieces = []
    totalPoints = 0
    run = True

def moveCalculator(holesFactor,linesFactor,heightFactor):
    global activePiece
    global pieces

    piece = tetramino(activePiece.win, activePiece.width,
                      cp.deepcopy(activePiece.setup), activePiece.color)
    validMoves = []

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
            validMoves.append(validMove(piece.x, piece.y, i, piece, pieces,holesFactor,linesFactor,heightFactor))
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
            return move


def applyMove(move):
    global activePiece
    global pieces

    if not move == None:
        while move.nRotation > 0:
            activePiece.rotate()
            move.nRotation -= 1
        activePiece.x = move.x
        activePiece.generator()
        while activePiece.isActive:
            activePiece.move(pieces)
            #draw()


def main(holesFactor,linesFactor,heightFactor,auto):
    global run
    global counter
    global buff
    global pieces
    global activePiece
    global prev

    activePiece = tetramino(win, size, shapes[buff], colors[buff])
    buff = rm.randrange(0, 7)

    prev = tetramino(win, size, shapes[buff], colors[buff])
    prev.x = overlay[1].x + (overlay[1].width-(size*len(shapes[buff][0])))//2
    prev.y = overlay[1].y + (overlay[1].height-(size*len(shapes[buff][0])))//2
    prev.generator()

    while not activePiece == 0:
        counter += 1
        if not len(pieces) == 0:
            cleanCheck(pieces)
        k = 0
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                     run = False
                     run = False
                if (event.key == pg.K_r):
                    activePiece.rotate()
                if event.key == pg.K_LEFT:
                    activePiece.left(pieces)
                if event.key == pg.K_RIGHT:
                    activePiece.right(pieces)
                if event.key == pg.K_DOWN:
                    activePiece.move(pieces)
        if (counter % 100) == 0:
            activePiece.move(pieces)
        if auto:
            applyMove(moveCalculator(holesFactor,linesFactor,heightFactor))
        else:
            draw()
            #clock.tick(1000)
        for piece in pieces:
            if piece.y <= 25:
                run = False
        if not activePiece.isActive:
            for tetra in activePiece.tetras:
                tetra.isActive = False
                pieces.append(tetra)
            activePiece = 0


def cleanCheck(pieces):
    global totalPoints
    grid = []
    rows = []
    points = 0

    for piece in pieces:
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
            for piece in pieces:
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
    while i < len(pieces):
        if not pieces[i].marked == 0 and pieces[i].marked < 70:
            while pieces[i].marked > 0:
                pieces[i].y += size
                pieces[i].marked -= 1

        elif pieces[i].marked >= 70:
            pieces.pop(i)

        else:
            i += 1

    return pieces

def draw():
    global pieces
    global activePiece
    global prev

    for over in overlay:
        over.draw()

    prev.draw()

    for piece in pieces:
        piece.draw()

    activePiece.draw()

    text = font.render('Points: ' + str(totalPoints),
                       True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.x, textRect.y = (600, 350)
    win.blit(text, textRect)
    pg.display.update()

    pg.display.flip()
    win.fill((20, 20, 20))

winX = 1050
winY = 1050
pg.init()
win = pg.display.set_mode((winX, winY))
pg.key.set_repeat(100, 50)
clock = pg.time.Clock()
size = 50
totalPoints = 0
run = True
prev = 0
pieces = []

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

buff = rm.randrange(0, 6)
activePiece = tetramino(win, size, shapes[buff], colors[buff])
counter = 0
overlay = [rect(win, 50, 25, winY-50, (0, 0, 0)),
           rect(win, 600, 100, 200, (0, 0, 0))]
overlay[0].width = 500

font = pg.font.Font('freesansbold.ttf', 32)

def game(holesFactor,linesFactor,heightFactor):
    while run:
        main(holesFactor,linesFactor,heightFactor,True)
    return totalPoints

if __name__ == '__main__':
    main(1,1,1,False)
        
