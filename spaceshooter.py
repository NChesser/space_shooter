import pygame, sys, random
from pygame.locals import *

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255 )

class Object(object):
    def draw(self, screen, shapes, colour):
        for s in shapes:
            pygame.draw.rect(screen, colour, s) 
    

class Ship(Object):
    def __init__(self):
        self.box = Rect((random.randrange(0,1150), random.randrange(0,750)), (50,50))
        self.colour = WHITE
    

class Enemey(Object):
    def __init__(self, name):
        self.name = name
        self.colour = (25,200,76)
        self.box = Rect((random.randrange(0,1150), random.randrange(0,750)), (20,20))
        self.xDir = 1
        self.yDir = 1
    
    def move_enemey(self, screen):
       
        self.box.x += self.xDir
        if self.box.x >= 1150 or self.box.x <= 0:
            self.xDir *= -1
        elif self.box.y >= 800 or self.box.y <= 0:
            self.yDir *= -1
    
    def switch_dir(self):
        self.xDir *= -1 
        self.yDir *= -1   
    

class Dasher(Enemey):    
    def __init__(self, name):
        super().__init__("Dasher"+str(name))

class Smasher(Enemey):    
    def __init__(self, name):
        super().__init__("Smasher"+str(name))
    
    def move_enemey(self, screen):
        self.box.y += self.yDir
        if self.box.y >= 750 or self.box.y <= 0:
            self.yDir *= -1
        
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((1200,800))
    pygame.key.set_repeat(5, 1)

    smashers = [Smasher(e) for e in range(20)]
    dashers = [Dasher(e) for e in range(20)]
    ship = Ship()


    while True: #main game loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # key movements
            elif event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    ship.box.y -=5
                if event.key == pygame.K_DOWN:
                    ship.box.y +=5
                if event.key == pygame.K_LEFT:
                    ship.box.x -=5
                if event.key == pygame.K_RIGHT:
                    ship.box.x +=5   
        
        screen.fill(BLACK)

        for s in smashers:
            s.draw(screen, [s.box], s.colour)
            s.move_enemey(screen)
            if s.box.collidelistall([x.box for x in smashers if x.name != s.name]) or s.box.collidelistall([x.box for x in dashers]):
                s.switch_dir()
            if s.box.colliderect(ship.box):
                smashers.remove(s)
                smashers.append(Smasher(random.randint(1,1111)))
        for d in dashers:
            d.draw(screen, [d.box], (200,10,55))
            d.move_enemey(screen)
            if d.box.collidelistall([x.box for x in smashers]) or d.box.collidelistall([x.box for x in dashers if x.name != d.name]):
                d.switch_dir()
            if d.box.colliderect(ship.box):
                dashers.remove(d)
                dashers.append(Dasher(random.randint(1,1111)))
               
        ship.draw(screen, [ship.box], ship.colour)

        pygame.display.update()


if __name__=='__main__':
    main()