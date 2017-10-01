from object import Object
import pygame
from pygame.locals import *

class Weapon(Object):
    def __init__(self, start_pos):
        self.speed = 2
        self.pos = start_pos
        self.box = Rect(self.pos[0], self.pos[1], 10, 10)

    def move(self):
        pass

    def check_collision(self, enemies):
        pass

    def explode(self):
        self.box.inflate_ip(20, 20)

class Regular(Weapon):
    def __init__(self, start_pos):
        super().__init__(start_pos)

    def move(self):
        self.box.y -= 10




