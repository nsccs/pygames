"""Entry point for the Asteroid clone game."""
import pygame
from time import sleep 
import math
import os

TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ROTATION_SPEED = 100
VELOCITY_INCREASE_ON_KEYPRESS = 20
CONSTANT_DECELERATION = -30


class Ship:
# TODO: Split into higher level class that takes in asset as argument (?)
    __slots__ = 'screen', 'pos', 'sprite', 'displayed_sprite', 'sprite_rect', 'direction', \
                'velocity_magnitude', 'velocity_direction', 'total_sprite_rotation', 'constant_deceleration'
    def __init__(self, screen):
        self.screen = screen
        self.sprite = pygame.image.load(os.path.join(TOP_DIR, 'assets/ship.png'))
        self.displayed_sprite = self.sprite
        self.sprite_rect = self.sprite.get_rect()
        
        starting_x = (screen.get_width() / 2) - self.sprite.get_rect().centerx
        starting_y = (screen.get_height() / 2) - self.sprite.get_rect().centery
        self.pos = pygame.Vector2(starting_x, starting_y)
        self.direction = math.pi / 2 # radians
        self.velocity_direction = self.direction # radians
        self.velocity_magnitude = 0
        
        self.total_sprite_rotation = 0 # degrees
        self.constant_deceleration = CONSTANT_DECELERATION

    def rotate_sprite(self):
        self.displayed_sprite = pygame.transform.rotate(self.sprite, self.total_sprite_rotation)

    def rotate(self, angle):
        self.direction += math.radians(angle)
        self.total_sprite_rotation += angle
        self.rotate_sprite()

    def calc_vector_from_angle_and_magnitude(self, magnitude):
        x = magnitude * math.cos(self.direction)
        y = magnitude * -1 * math.sin(self.direction) # because y=0 is at the top of the screen
        return pygame.Vector2(x, y)

    def move_forward(self, amount):
        pos_change_vector = self.calc_vector_from_angle_and_magnitude(amount)
        self.pos += pos_change_vector

    def slow_down(self, dt):
        self.velocity_magnitude += self.constant_deceleration * dt
        if self.velocity_magnitude < 0:
            self.velocity_magnitude = 0

    

class Game:
    """Game class encapsulates functionality to make the game run."""

    # slots attribute allows one to explicitly state expected attributes
    # benefits: faster access and space (memory) savings
    # update as needed
    __slots__ = 'screen', 'dt', 'clock', 'ship'

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

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.ship.velocity_magnitude += VELOCITY_INCREASE_ON_KEYPRESS
        if keys[pygame.K_s]:
            self.ship.velocity_magnitude -= VELOCITY_INCREASE_ON_KEYPRESS
        if keys[pygame.K_LEFT]:
            self.ship.rotate(ROTATION_SPEED * self.dt)
        if keys[pygame.K_RIGHT]:
            self.ship.rotate(-1 * ROTATION_SPEED * self.dt)

    def process_game_logic(self):
        """Implement and update docstring and return type"""
        self.ship.move_forward(self.ship.velocity_magnitude * self.dt)
        self.ship.slow_down(self.dt)

    def draw_game_elements(self):
        """Implement and update docstring and return type"""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.ship.displayed_sprite, self.ship.pos)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
