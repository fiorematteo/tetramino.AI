#esterni
from random import randint
#interni
from tetramino import *

class Tetris:
    
    font = None
    clock = pg.time.Clock()

    def __init__(self):
        self.win = None
        self.run = True
        self.activePiece = None
        self.nextPiece = None
        self.pieces = []
        self.points = 0
        self.clockSpeed = 200

    def start(self):
        pg.init()
        self.win = pg.display.set_mode((winX, winY))
        Tetris.font = pg.font.Font('freesansbold.ttf', 32)
        self.game()
        print("gameover")

    def drawGUI(self):
        pg.draw.rect(self.win, (255,255,255), (50, 25, 500, winY-50), 1)
        pg.draw.rect(self.win, (255,255,255), (600, 100, 200, 200), 1)

    def drawTEXT(self):
        text = Tetris.font.render(f'Points: {self.points}',True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.x, textRect.y = (600, 350)
        self.win.blit(text, textRect)

    def drawAll(self):
        self.drawGUI()
        for piece in self.pieces:
            piece.draw()
        self.activePiece.draw()
        self.nextPiece.draw()
        self.drawTEXT()
        pg.display.flip()
        self.win.fill((20,20,20))
        Tetris.clock.tick(self.clockSpeed)
        
    def swapPieces(self):
        for tetra in self.activePiece.tetras:
            self.pieces.append(tetra)
        self.activePiece = self.nextPiece
        self.nextPiece = tetramino(self.win, randint(0,6))
        self.nextPiece.x = 600
        self.nextPiece.y = 100

    def eventLoop(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.run = False
                elif (event.key == pg.K_r):
                    self.activePiece.rotate()
                elif event.key == pg.K_LEFT:
                    self.activePiece.left(self.pieces)
                elif event.key == pg.K_RIGHT:
                    self.activePiece.right(self.pieces)
                elif event.key == pg.K_DOWN:
                    self.activePiece.move(self.pieces)
            elif event.type == pg.QUIT:
                slef.run = False

    def lineClear(self):
        lines={}
        points = 0
        removedLines = []
        for piece in self.pieces:
            if piece.y in lines:
                lines[piece.y]+=1
            else:
                lines[piece.y] = 1

        for piece in self.pieces:
            if lines[piece.y] == 10:
                if not piece.y in removedLines:
                    removedLines.append(piece.y)
                piece.marked == True
                points += 1
        points /= 10

        for piece in self.pieces:
            if piece.marked == True:
                pieces.remove(piece)

        lines = dict(filter(lambda elem: elem == 10,lines.items()))

        for line in lines:
            for piece in self.pieces:
                if piece.y > lines[line]:
                    piece.y += piece.height

        
        if points == 1:
            self.points += 40
        elif points == 2:
            self.points += 100
        elif points == 3:
            self.points += 300
        elif points == 4:
            self.points += 1200


    def game(self):
        self.nextPiece = tetramino(self.win, randint(0, 6))
        self.nextPiece.x = 600
        self.nextPiece.y = 100
        self.activePiece = tetramino(self.win, randint(0, 6))
        counter = 0
        while self.run:
            self.eventLoop()

            if not self.activePiece.gameOver():
                self.run = False

            if self.activePiece.isActive == False:
                self.swapPieces()
            if (counter % 100) == 0:
                self.activePiece.move(self.pieces)
            counter += 1

            self.lineClear()
            self.drawAll()

Tetris().start()
