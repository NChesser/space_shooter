import pygame, random
from pygame.locals import *
from object import Object
from constants import *

class Enemey(Object):
    def __init__(self, name):
        self.name = name
        self.width = 20
        self.height = 20
        self.colour = (25, 200, 76)
        self.box = Rect(random.randrange(0, WIDTH-self.width), random.randrange(0, HEIGHT-self.height), self.width, self.height)
        self.xDir = 5
        self.yDir = 5

    def move_enemey(self):
        self.box.x += self.xDir
        if self.box.x >= WIDTH-self.width or self.box.x <= 0:
            self.xDir *= -1
        elif self.box.y >= HEIGHT-self.height or self.box.y <= 0:
            self.yDir *= -1

    def switch_dir(self):
        self.xDir *= -1
        self.yDir *= -1

    def inflate(self):
        pass

class Dasher(Enemey):
    def __init__(self, name):
        super().__init__("Dasher" + str(name))
        self.width = 30
        self.box = Rect(random.randrange(0, WIDTH-self.width), random.randrange(0, HEIGHT-self.height), self.width, self.height)
        self.colour = pygame.Color("green")

class Smasher(Enemey):
    def __init__(self, name):
        super().__init__("Smasher" + str(name))
        self.colour = pygame.Color("blue")

    def move_enemey(self):
        self.box.y += self.yDir
        if self.box.y >= HEIGHT-self.height or self.box.y <= 0:
            self.yDir *= -1

    #def inflate(self):
        #if self.box.width < 25:
            #self.box.inflate_ip(1, 2)

class Stalker(Enemey):
    def __init__(self, name):
        super().__init__("Stalker" + str(name))
        self.colour = pygame.Color("red")
        self.box = Rect(random.randrange(0, WIDTH-self.width), -30, self.width, self.height)

    def move_enemey(self, player_xpos, player_ypos, stalkers):

        if not self.box.collidelistall([x.box for x in stalkers if self.name != x.name]):
            if self.box.x < player_xpos:
                self.box.x += 2
            elif self.box.x > player_xpos:
                self.box.x -= 2

            if self.box.y < player_ypos:
                self.box.y += 2
            elif self.box.y > player_ypos:
                self.box.y -= 2
        else:
            self.box.x += random.randrange(-10,10)
            self.box.y += random.randrange(-10,10)

    def explode(self):
        self.box.inflate_ip(5,5)

