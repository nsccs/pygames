from typing import List
import pygame
import math
from image_loader import ImageLoader

"""
Explanation of coordinate system:

Pygame uses x and y to store coordinates.
An important difference between pygame and how coordinates work in math
is that in pygame y = 0 is at the top of the screen.
That means adding to y will bring something lower on the screen, which is confusing.

Explanation of vectors:

In pygame, a Vector2 is a way of storing an x and y variable in a single place.
This program uses Vector2s to store the ship's position and velocity.
It's convenient to store the ship's velocity as x and y in a single vector and
to add it to the ship's position every frame. The position is also a Vector2 and Vector2s can be conveniently added together.
The x and y in a vector make up a triangle. The hypotenuse of that triangle is the magnitude of the vector.
"""


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
FRAME_RATE = 60

APPROX_TIME_PER_FRAME = round(1 / FRAME_RATE, 3)

# These constants are used a lot, so it seems faster to not have to multiply them by delta time every frame.
ROTATION_SPEED = 200 * APPROX_TIME_PER_FRAME
CONSTANT_DECELERATION = 1 * APPROX_TIME_PER_FRAME
MAX_SPEED = 300 * APPROX_TIME_PER_FRAME
VELOCITY_INCREASE_ON_KEYPRESS = 10 * APPROX_TIME_PER_FRAME


def rot_center(image, angle):
    """
    Rotate an image while keeping its center and size.
    https://www.pygame.org/wiki/RotateCenter?parent=CookBook
    """
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Projectile:
    __slots__ = ("pos", "direction", "velocity_vector", "rotation", "sprite", "cleanup")

    def __init__(self, pos, direction, velocity_vector, rotation):
        self.pos = pos.copy()
        self.direction = direction
        self.velocity_vector = velocity_vector.copy()
        self.cleanup = False
        self.sprite = rot_center(
            ImageLoader.load_sprite("assets/projectile.png"), rotation
        )


class Entity:
    __slots__ = (
        "screen",
        "pos",
        "sprite",
        "displayed_sprite",
        "hitbox",
        "direction",
        "velocity_vector",
        "total_sprite_rotation",
    )

    def __init__(self, screen, sprite, hitbox):
        """
        Init entity with screen size, image representation, hit box, starting coordinates, start direction,
        velocity vector, and total sprite rotation.
        """
        self.screen = screen
        # the sprite has to be square to allow rotation around its center, so the hitbox is an image with smaller dimensions
        self.sprite = ImageLoader.load_sprite(sprite)
        self.displayed_sprite = (
            self.sprite
        )  # this variable allows the original sprite to be maintained when the entity rotates
        self.hitbox = ImageLoader.load_sprite(hitbox).get_rect()

        starting_x = (screen.get_width() / 2) - self.sprite.get_rect().centerx
        starting_y = (screen.get_height() / 2) - self.sprite.get_rect().centery
        self.pos = pygame.Vector2(starting_x, starting_y)
        self.direction = (
            math.pi / 2
        )  # radians. should be the same starting angle of the sprite
        self.velocity_vector = pygame.Vector2(0, 0)
        self.total_sprite_rotation = 0  # degrees

    def rotate_sprite(self):
        """Rotate sprite."""
        self.displayed_sprite = rot_center(self.sprite, self.total_sprite_rotation)

    def rotate(self, angle: float | int):
        """Rotate entity 'angle' degrees"""
        self.direction += math.radians(angle)
        self.total_sprite_rotation += angle
        self.rotate_sprite()

    def calc_forward_facing_velocity(self, magnitude: float | int) -> pygame.Vector2:
        """Creates a Vector2 in the direction the entity is facing with magnitude 'magnitude'."""
        x = magnitude * math.cos(self.direction)
        y = (
            magnitude * -1 * math.sin(self.direction)
        )  # because y=0 is at the top of the screen
        return pygame.Vector2(x, y)



    def add_forward_velocity(self, amount: float | int):
        """Adds 'amount' to the entity's velocity in the same direction it's currently facing."""
        forward_velocity_vector = self.calc_forward_facing_velocity(amount)
        self.velocity_vector += forward_velocity_vector
        self.velocity_vector = self.velocity_vector.clamp_magnitude(MAX_SPEED)

    def move(self):
        """Moves the ship by its velocity."""
        self.pos += self.velocity_vector

    def calc_drag(self, magnitude: float | int) -> pygame.Vector2:
        """Find a vector that's the opposite of the entity's velocity vector in order t"""
        if self.velocity_vector.magnitude() > 0:
            acceleration_vector = (
                self.velocity_vector.normalize() * magnitude * -1
            )  # -1 makes it the opposite direction of the velocity
            return acceleration_vector
        else:
            return pygame.Vector2(0, 0)

    def slow_down(self, magnitude: float | int):
        """Calculate and set velocity vector."""
        drag_vector = self.calc_drag(magnitude)
        self.velocity_vector += drag_vector

    def keep_within_borders(self):
        # have to use hitbox in some cases because center of pos is on the top left of entity sprite
        pad = 10
        # left
        if self.pos.x + self.hitbox.right + pad < 0:
            self.pos = pygame.Vector2(SCREEN_WIDTH, self.pos.y)
        # right
        elif self.pos.x - pad > SCREEN_WIDTH:
            self.pos = pygame.Vector2(0, self.pos[1])
        # top
        elif self.pos.y + pad + self.hitbox.bottom < 0:
            self.pos = pygame.Vector2(self.pos.x, SCREEN_HEIGHT)
        # bottom
        elif self.pos.y - pad > SCREEN_HEIGHT:
            self.pos = pygame.Vector2(self.pos.x, 0)


class Game:
    """Game class encapsulates functionality to make the game run."""

    __slots__ = 'screen', 'dt', 'clock', 'ship', 'projectiles'

    def __init__(self, title: str = "NSCCSC Asteroid Clone") -> None:
        """Init Game with initial pygame, display caption, and display size."""
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((0, 0, 0))
        self.dt = 0  # delta time
        self.clock = pygame.time.Clock()
        self.ship = Entity(self.screen, "assets/ship.png", "assets/shiphitbox.png")
        self.projectiles: List[Projectile] = []

    def run(self) -> None:
        while True:
            self.handle_input()
            self.process_game_logic()
            self.draw_game_elements()

            # use delta time, which is the amount of time that has passed between each frame.
            # this allows behaviour like velocity to be based on actual time passed instead of the amount of frames.
            seconds_per_millisecond = 1000
            self.dt = self.clock.tick(FRAME_RATE) / seconds_per_millisecond  # NOTE: not currently used

    def handle_input(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # check for keys within get_pressed() to continuously check which keys are pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.projectiles.append(
                Projectile(
                    self.ship.pos,
                    self.ship.direction,
                    self.ship.calc_forward_facing_velocity(3),
                    self.ship.total_sprite_rotation,
                )
            )
        if keys[pygame.K_w]:
            # multiply by dt to make the increase based on the amount of time that has passed between frames
            self.ship.add_forward_velocity(VELOCITY_INCREASE_ON_KEYPRESS)
        if keys[pygame.K_LEFT]:
            self.ship.rotate(ROTATION_SPEED)
        if keys[pygame.K_RIGHT]:
            self.ship.rotate(-1 * ROTATION_SPEED)
        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            pygame.quit()
            quit()

    def process_game_logic(self):
        self.ship.move()
        self.ship.slow_down(CONSTANT_DECELERATION)
        self.ship.keep_within_borders()
        self.move_projectiles()

    def draw_game_elements(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.ship.displayed_sprite, self.ship.pos)
        self.draw_projectiles()
        pygame.display.flip()

    def move_projectiles(self):
        for p in self.projectiles:
            if p.pos.x < 0 or p.pos.x > SCREEN_WIDTH:
                p.cleanup = True
            elif p.pos.y < 0 or p.pos.y > SCREEN_HEIGHT:
                p.cleanup = True
            p.pos += p.velocity_vector

    def cleanup_projectiles(self):
        self.projectiles = list(filter(lambda p: p.cleanup == False, self.projectiles))

    def draw_projectiles(self):
        self.cleanup_projectiles()
        for p in self.projectiles:
            self.screen.blit(p.sprite, p.pos)


if __name__ == "__main__":
    game = Game()
    game.run()
