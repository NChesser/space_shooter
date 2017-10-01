import sys, pygame
from object import Object
from ship import Ship
from enemey import *
from weapons import *


class Game(object):
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self):
        """Switch to the next game state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        """
        Check for state flip and update active state
        dt: milliseconds since last frame

        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        pygame.key.set_repeat(1, 1)

        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()


class GameState(object):
    """
    parent class for individual game states
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 50)

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        persistent: a dict passed from state to state
        """
        self.persist = persistent

    def get_event(self, event):
        """
        Handle a single event passed by the Game object
        """
        pass

    def update(self, dt):
        """
        Update the state. called by the Game object once per frame.

        dt: time since last frame
        """
        pass

    def draw(self, surface):
        """
        Draw everything to the screen
        """
        pass

class SplashScreen(GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.title = self.font.render("Press Enter to Start", True, pygame.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "Gameplay"

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                self.persist["screen_color"] = "gold"
                self.title = self.font.render("Press Enter to Start", True, pygame.Color("red"))
                self.done = True
            if event.key == pygame.K_SPACE:
                self.next_state = "Asteroids"
                self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.player = Ship()
        self.enemies = []
        self.stalkers = []
        self.bullets = []
        self.screen_color = pygame.Color("black")
        self.next_state = "Splash"
        self.score = 0
        self.score_title = self.font.render("Score: " + str(self.score), True, pygame.Color("dodgerblue"))
        self.health_title = self.font.render("Health: " + str(self.player.health), True, pygame.Color("dodgerblue"))

    def startup(self, persistent):
        self.persist = persistent
        smashers = [Smasher(e) for e in range(10)]
        dashers = [Dasher(e) for e in range(10)]
        self.stalkers = [Stalker(e) for e in range(10)]
        self.enemies = smashers + dashers
        self.score = 0
        self.delay = 5

    def get_event(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.move_horizontal(5)
        if keys[pygame.K_LEFT]:
            self.player.move_horizontal(-5)
        if keys[pygame.K_UP]:
            self.player.move_vertical(-5)
        if keys[pygame.K_DOWN]:
            self.player.move_vertical(5)
        if keys[pygame.K_ESCAPE]:
            self.done = True
        if keys[pygame.K_SPACE]:
            if self.player.weapon == "Regular" and self.delay == 5:
                self.delay = 0
                self.bullets.append(Regular([self.player.shape[0].x, self.player.shape[0].y]))
                self.bullets.append(Regular([self.player.shape[0].x + self.player.width - 10, self.player.shape[0].y]))
                self.bullets.append(Regular([self.player.shape[0].x + 90, self.player.shape[5].y]))
                self.bullets.append(Regular([self.player.shape[0].x + 50, self.player.shape[5].y]))
            self.delay += 1

        if event.type == pygame.QUIT:
            self.quit = True

    def update(self, dt):
        for e in self.enemies:
            e.move_enemey()
            if e.box.collidelistall([x.box for x in self.enemies if x.name != e.name]):
                e.switch_dir()
                e.inflate()
            if e.box.collidelistall(self.player.shape):
                self.enemies.remove(e)
                self.enemies.append(Smasher(random.randint(1, 1111)))
                self.score += 1
                self.score_title = self.font.render("Score: " + str(self.score), True, pygame.Color("dodgerblue"))

        for s in self.stalkers:
            s.move_enemey(self.player.shape[0].x, self.player.shape[0].y, self.stalkers)
            if s.box.collidelistall(self.player.shape):
                s.explode()
                if s.box.width > 50:
                    self.stalkers.remove(s)
                    self.player.health -= 1
                    self.health_title = self.font.render("Health: " + str(self.player.health), True, pygame.Color("dodgerblue"))
                    self.stalkers.append(Stalker(random.randrange(1,10000)))

        for b in self.bullets:
            b.move()
            for e in self.enemies:
                if b.box.colliderect(e.box):
                    b.explode()
                    self.enemies.remove(e)
                    self.score += 1
                    self.title = self.font.render("Score: " + str(self.score), True, pygame.Color("orange"))
            for s in self.stalkers:
                if b.box.colliderect(s.box):
                    b.explode()
                    self.stalkers.remove(s)
                    self.stalkers.append(Stalker(random.randrange(1,10000)))
                    self.score += 1
                    self.title = self.font.render("Score: " + str(self.score), True, pygame.Color("yellow"))

            if b.box.y < 0:
                self.bullets.remove(b)

        if len(self.enemies) == 0:
            self.next_state = "Splash"
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.player.draw(surface, self.player.shape, self.player.colour)
        for e in self.enemies:
            e.draw(surface, [e.box], e.colour)
        for s in self.stalkers:
            s.draw(surface, [s.box], s.colour)
        for b in self.bullets:
            b.draw(surface, [b.box], pygame.Color("gold"))
        surface.blit(self.score_title, (10, 10))
        surface.blit(self.health_title, (WIDTH - 170, 10))
