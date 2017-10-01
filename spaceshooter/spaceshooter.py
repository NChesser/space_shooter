import pygame
import sys
from game_states import *
from constants import *
from asteroid_state import *

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    states = {"Splash": SplashScreen(), "Gameplay": Gameplay(), "Asteroids": Asteroids()}
    game = Game(screen, states, "Splash")
    game.run()
    pygame.quit()
    sys.exit()
