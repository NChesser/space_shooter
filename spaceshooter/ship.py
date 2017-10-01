import pygame, random
from pygame.locals import *
from reportlab.graphics.shapes import Polygon

from object import Object
from weapons import *
from constants import *

class Ship(Object):
    def __init__(self):
        self.width = 150
        self.height = 12
        self.health = 5
        self.shape = []
        self.shape.append(Rect(WIDTH/2-self.width/2, HEIGHT-12, self.width, self.height))
        self.shape.append(Rect(WIDTH/2-self.width/2, HEIGHT-20, 10, 10))
        self.shape.append(Rect(WIDTH/2-self.width/2+self.width-10, HEIGHT-20, 10, 10))
        self.shape.append(Rect(WIDTH/2-75/2, HEIGHT-20, 75, 25))
        self.shape.append(Rect(WIDTH/2-50/2, HEIGHT-30, 50, 20))
        self.shape.append(Rect(WIDTH/2-30/2, HEIGHT-40, 30, 20))
        self.colour = pygame.Color("white")
        self.weapon = "Regular"

    def move_horizontal(self, event):
        if self.shape[0].x > 0 and event < 0:
            for s in self.shape:
                s.x += event
        elif self.shape[0].x < WIDTH - self.shape[0].width and event > 0:
            for s in self.shape:
                s.x += event

    def move_vertical(self, event):
        if self.shape[0].y > 0 and event < 0:
            for s in self.shape:
                s.y += event
        elif self.shape[0].y < HEIGHT - self.shape[0].height and event > 0:
            for s in self.shape:
                s.y += event


class Asteroid_Ship(object):
    def __init__(self):
        self.x = 20
        self.y = 20
        self.angle = 5
        self.shape = [(self.x, self.y), (self.x-20, self.y+20), (self.x+20, self.y+20)]

    def update(self):
        pass

    def draw(self, surface):
        pass


