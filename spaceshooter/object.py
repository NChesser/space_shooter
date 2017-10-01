import pygame
from pygame.locals import *

class Object(object):
    def draw(self, screen, shapes, colour):
        for s in shapes:
            pygame.draw.rect(screen, colour, s)
