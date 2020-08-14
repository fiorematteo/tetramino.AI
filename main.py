#esterni
from random import randint
#interni
from tetramino import *

class Tetris:
    
    def __init__(self):
        self.win = None
        self.run = True
        self.activePiece = None
        self.nextPieceNumb = randint(0, 6)
    
    def start(self):
        pg.init()
        self.win = pg.display.set_mode((winX, winY))
        game()

    def drawGUI(self):
        pg.draw.rect(self.win, (255,255,255), (50, 25, 500, winY-50), 1)
        pg.draw.rect(self.win, (255,255,255), (600, 100, 200, 200), 1)

    def eventLoop(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.run = False
                if (event.key == pg.K_r):
                    self.activePiece.rotate()
                if event.key == pg.K_LEFT:
                    self.activePiece.left(self.pieces)
                if event.key == pg.K_RIGHT:
                    self.activePiece.right(self.pieces)
                if event.key == pg.K_DOWN:
                    self.activePiece.move(self.pieces)

    def game(self):
        self.activePiece = tetramino(self.win, randint(0, 6))
        while self.run:
