import pygame as pg
from rect import *


class tetramino:

    def __init__(self, win, size, setup, color):
        self.win = win
        self.width = size
        self.height = size
        self.isActive = True
        self.setup = setup
        self.color = color
        self.tetras = []
        self.x = 250
        self.y = 25
        self.generator()

    def draw(self):
        minX = 500
        maxX = 0
        for tetra in self.tetras:
            pg.draw.rect(self.win, tetra.color,
                         (tetra.x, tetra.y, tetra.width, tetra.height), 0)
            pg.draw.rect(self.win, (255, 255, 255),
                         (tetra.x, tetra.y, tetra.width, tetra.height), 1)
            minX = tetra.x if tetra.x < minX else minX
            maxX = tetra.x if tetra.x > maxX else maxX
        if self.x < 500:
            pg.draw.line(self.win, (255,255,255),(minX,25),(minX,1025))
            pg.draw.line(self.win, (255,255,255),(maxX+self.width,25),(maxX+self.width,1025))

    def generator(self):
        self.tetras = []
        x = 0
        y = 0
        while y < len(self.setup):
            while x < len(self.setup[0]):
                if self.setup[y][x]:
                    self.tetras.append(rect(
                        self.win, self.x+(x*self.width), self.y+(y*self.height), self.height, self.color))
                x += 1
            x = 0
            y += 1

    def rotate(self):
        self.setup = list(zip(*self.setup[::-1]))
        for tup in self.setup:
            self.setup[self.setup.index(tup)] = list(tup)
        self.generator()

        for tetra in self.tetras:
            if tetra.x < 50:
                for tetra in self.tetras:
                    tetra.x += self.width
                self.x += self.width
            if tetra.x >= 550:
                for tetra in self.tetras:
                    tetra.x -= self.width
                self.x -= self.width

    def move(self, pieces):
        if not self.collisions(pieces) and self.isActive:
            for tetra in self.tetras:
                tetra.y = tetra.y + self.height
            self.y += self.height

    def collisions(self, pieces):
        for tetra in self.tetras:
            for piece in pieces:
                if piece.y == tetra.y+self.height and piece.x == tetra.x:
                    self.isActive = False
                    return True
            if tetra.y + self.height == winY-25:
                self.isActive = False
                return True
        return False

    def left(self, pieces):
        for tetra in self.tetras:
            for piece in pieces:
                if piece.y == tetra.y and piece.x == tetra.x - self.width:
                    self.isActive = False
            if tetra.x == 50:
                return 0

        if self.isActive:
            for tetra in self.tetras:
                tetra.x -= self.width
            self.x -= self.width

    def right(self, pieces):
        for tetra in self.tetras:
            for piece in pieces:
                if piece.y == tetra.y and piece.x == tetra.x + self.width:
                    self.isActive = False
            if tetra.x + self.width == 550:
                return 0

        if self.isActive:
            for tetra in self.tetras:
                tetra.x += self.width
            self.x += self.width
