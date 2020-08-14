import pygame as pg
winX = 1050
winY = 1050


class rect:

    def __init__(self, win, x, y, size, color):
        self.win = win
        self.x = x
        self.y = y
        self.width = size
        self.height = size
        self.color = color
        self.isActive = True
        self.marked = 0

    def draw(self):
        pg.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height), 0)
        pg.draw.rect(self.win, (255,255,255), (self.x, self.y, self.width, self.height), 1)

    def collisions(self, pieces):
        nextPos = self.y + self.height
        for piece in pieces:
            if nextPos == piece.y and self.x == piece.x:
                self.isActive = False
        if self.y >= winY - self.height:
            self.isActive = False

    def move(self):
        if self.isActive:
            self.y += self.height
