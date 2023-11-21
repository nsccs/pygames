from random import randint, randrange
from typing import List
import pygame


class Star:
    """A single star."""

    __slots__ = 'screen', 'color', 'x', 'y', 'center', 'radius'

    def __init__(
            self,
            screen: pygame.Surface,
            color: str,
            x: int,
            y: int,
            radius:int,
    ) -> None:
        """Init with game screen, color, x ,y which represent center of the circle and radius."""
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.center = (x, y)
        self.radius = radius

    def draw(self) -> None:
        """Draw self onto the screen."""
        pygame.draw.circle(self.screen, self.color, self.center, self.radius)


class Background:
    """Logic for any code relating to the background of the game."""

    __slots__ = 'screen', 'stars'

    def __init__(self, screen) -> None:
        """Init with screen and empty list container for stars."""
        self.screen = screen
        self.stars = list()

    def create_stars(self, number: int) -> List[Star]:
        """Create a number of Star objects and append to self.stars."""
        for i in range(number):
            x = randint(1, self.screen.get_width())
            y = randint(1, self.screen.get_height())
            radius = randrange(1, 3)
            self.stars.append(Star(self.screen, 'white', x, y, radius))
        return self.stars

    def draw_stars(self) -> None:
        """Draw each Star stored in self.stars."""
        for star in self.stars:
            star.draw()