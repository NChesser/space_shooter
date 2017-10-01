from game_states import Game, GameState
from ship import Asteroid_Ship
from pygame.locals import *
from pygame.gfxdraw import *
import pygame

class Asteroids(GameState):
    def __init__(self):
        super(Asteroids, self).__init__()
        self.title = self.font.render("Asteroids", True, pygame.Color("Green"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.ship = Asteroid_Ship()

    def startup(self, persistent):
        pass

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.ship.y -=5
                self.ship.update()
            if event.key == pygame.K_DOWN:
                self.ship.y += 5
                self.ship.update()
            if event.key == pygame.K_RIGHT:
                self.ship.angle += 1
                self.ship.update()
            if event.key == pygame.K_LEFT:
                self.ship.angle -= 1
                self.ship.update()


    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)
        pygame.draw.polygon(surface, pygame.Color("white"), self.ship.shape)

