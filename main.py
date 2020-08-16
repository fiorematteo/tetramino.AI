#esterni
from random import randint
#interni
from tetramino import *
from AI import *

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
        self.clockSpeed = 100
        self.nextNumber = 0

    def start(self,ai=False,isDrawing=True):
        if isDrawing:
            pg.init()
            self.win = pg.display.set_mode((winX, winY))
            Tetris.font = pg.font.Font('freesansbold.ttf', 32)
            pg.key.set_repeat(100, 50)
        return self.game(ai,isDrawing)

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
        self.generateNextPiece()

    def generateNextPiece(self):
        self.activePiece = tetramino(self.win, self.nextNumber)
        self.nextNumber = randint(0,6)
        self.nextPiece = tetramino(self.win, self.nextNumber)
        self.nextPiece.x = 600
        self.nextPiece.y = 100
        self.nextPiece.generator()
        
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
        for piece in self.pieces:
            if piece.y in lines:
                lines[piece.y]+=1
            else:
                lines[piece.y] = 1

        for piece in self.pieces:
            if lines[piece.y] == 10:
                piece.marked = True
                points += 1
        points /= 10

        i = 0
        while i < len(self.pieces):
            if self.pieces[i].marked:
                self.pieces.pop(i)
            else:
                i += 1

        lines = {k: v for k, v in lines.items() if v == 10}

        for piece in self.pieces:
            t = piece.y
            for line in lines:
                if t < line:
                    piece.y += piece.height

        
        if points == 1:
            self.points += 40
        elif points == 2:
            self.points += 100
        elif points == 3:
            self.points += 300
        elif points == 4:
            self.points += 1200

    def gameOver(self):
        for piece in self.pieces:
            if piece.y <= 25:
                return False
        return True

    def game(self, ai, isDrawing):
        self.nextNumber = randint(0,6)
        self.generateNextPiece()
        counter = 0
        if ai:
            self.clockSpeed = 0
        while self.run:
            if isDrawing:
                self.eventLoop()

            if not self.gameOver():
                self.run = False
            
            if ai:
                ai.moveCalculator(self.activePiece, self.pieces)
                ai.applyMove(self.activePiece, self.pieces)

            if self.activePiece.isActive == False:
                self.swapPieces()
            if (counter % 100) == 0:
                self.activePiece.move(self.pieces)
            counter += 1

            
            self.lineClear()
            if isDrawing:
                self.drawAll()
        
        if ai:
            return self.points

if __name__ == '__main__':
    Tetris().start()
