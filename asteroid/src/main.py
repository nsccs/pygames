"""Entry point for the Asteroid clone game."""
import pygame
from time import sleep 
import math
import os
TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Ship:
# TODO: Split into higher level class that takes in asset as argument (?)
    __slots__ = 'screen', 'pos', 'sprite', 'sprite_rect'
    def __init__(self, screen):
        self.screen = screen
        self.sprite = pygame.image.load(os.path.join(TOP_DIR, 'assets/ship.png'))
        self.sprite_rect = self.sprite.get_rect()
        self.pos = pygame.Vector2((screen.get_width() / 2) - self.sprite_rect.centerx, (screen.get_height() / 2) - self.sprite_rect.centery)


    def move_forward(self):
        pass


class Game:
    """Game class encapsulates functionality to make the game run."""

    # slots attribute allows one to explicitly state expected attributes
    # benefits: faster access and space (memory) savings
    # update as needed
    __slots__ = 'screen', 'dt', 'clock', 'shipvelocity', 'ship'

    def __init__(self, title: str = "NSCCSC Asteroid Clone") -> None:
        """Init Game with initial pygame, display caption, and display size."""
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((960, 720))
        self.dt = 0 # delta time
        self.clock = pygame.time.Clock()
        self.ship = Ship(self.screen)

    def run(self) -> None:
        while True:
            # self.handle_events()
            self.handle_input()
            self.process_game_logic()
            self.draw_game_elements()
            self.dt = self.clock.tick(60) / 1000
            

    def handle_input(self):
        """Implement and update docstring and return type"""
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # if event.type == pygame.MOUSEMOTION:
            #     mouseloc = pygame.mouse.get_pos()
            #     pygame.draw.circle(self.screen, (255, 255, 255), mouseloc, mouseloc[0] // 2, width=mouseloc[1] // 10)
            #     pygame.display.update()

            if event.type == pygame.K_w:
                self.ship.move_forward()

    def process_game_logic(self):
        """Implement and update docstring and return type"""
        

    def draw_game_elements(self):
        """Implement and update docstring and return type"""
        self.screen.fill((0, 0, 0))
        # pygame.draw.circle(self.screen, (255, 255, 255), self.ship.pos, 10)
        self.screen.blit(self.ship.sprite, self.ship.pos)
        pygame.display.flip()
        
        # pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
