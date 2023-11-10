"""Entry point for the Asteroid clone game."""
import pygame


class Game:
    """Game class encapsulates functionality to make the game run."""

    # slots attribute allows one to explicitly state expected attributes
    # benefits: faster access and space (memory) savings
    # update as needed
    __slots__ = 'screen'

    def __init__(self, title: str = "NSCCSC Asteroid Clone") -> None:
        """Init Game with initial pygame, display caption, and display size."""
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((800, 600))

    def run(self) -> None:
        while True:
            self.handle_input()
            self.process_game_logic()
            self.draw_game_elements()

    def handle_input(self):
        """Implement and update docstring and return type"""
        pass

    def process_game_logic(self):
        """Implement and update docstring and return type"""
        pass

    def draw_game_elements(self):
        """Implement and update docstring and return type"""
        pass


if __name__ == "__main__":
    game = Game()
    game.run()
