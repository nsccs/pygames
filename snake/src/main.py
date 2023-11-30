import pygame
import random
import snake_ui
from typing import Tuple


class Fruit:
    """Fruit class has a position and a color."""
    __slots__ = 'position', 'color'

    def __init__(self, position: Tuple[int, int], color=(255, 0, 0)) -> None:
        """Init with position and color."""
        self.position = position
        self.color = color


class Snake:
    def __init__(self, pos, direction, start_length=3, color=(255, 255, 255)):
        self.pos = pos
        self.parts = [pos]

        # how many bodyparts it can grow
        # usually only 0 or 1
        self.grow_count = start_length
        self.color = color
        self.direction = direction

    def update_snake(self):
        tail = self.parts[-1]

        # Updating the bodyparts
        partcopy = self.parts.copy()
        for part in range(len(partcopy) - 1):
            self.parts[part + 1] = partcopy[part]

        # Growing a new bodypart
        if self.grow_count > 0:
            self.parts.append(tail)
            self.grow_count -= 1

        head_pos = self.parts[0]
        head_pos = (head_pos[0] + self.direction[0], head_pos[1] + self.direction[1])
        self.parts[0] = head_pos

    def grow_snake(self):
        self.grow_count += 1


class Game:
    def __init__(
            self,
            grid_size=(32, 32),
            square_size=16,
            speed=20,
            background_color=(0, 0, 0)
    ):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.grid_size = grid_size
        self.square_size = square_size
        self.screen_w = grid_size[0] * square_size
        self.screen_h = grid_size[1] * square_size
        self.speed = speed
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.screen.fill(background_color)
        self.fps = pygame.time.Clock()
        self.snake = Snake((16, 16), (1, 0))
        self.fruit = Fruit(position=self.generate_random_coords())

    def generate_random_coords(self) -> Tuple[int, int]:
        """Generate random x and y coordinates within the grid constraints and return the coordinates as a tuple."""
        x_coord = random.randint(0, self.grid_size[0] - 1)
        y_coord = random.randint(0, self.grid_size[1] - 1)
        return (x_coord, y_coord)

    def run(self):
        while True:
            self.fps.tick(self.speed)
            self.get_input()
            self.update_game()
            self.draw_game()

    def get_input(self):
        newdir = self.snake.direction
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    newdir = (0, -1)
                if event.key == pygame.K_DOWN:
                    newdir = (0, 1)
                if event.key == pygame.K_LEFT:
                    newdir = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    newdir = (1, 0)
        # This part of the code is so that the player cant flip the snake
        if newdir[0] != 0:
            if newdir[0] != self.snake.direction[0] * -1:
                self.snake.direction = newdir
        else:
            if newdir[1] != self.snake.direction[1] * -1:
                self.snake.direction = newdir

    # Updates the position of the snake, and checks other things
    def update_game(self):
        self.snake.update_snake()
        # If the snake has collided with itself
        if self.snake.parts[0] in self.snake.parts[1:]:
            quit()
        # If the snake has collided with the wall
        if not 0 <= self.snake.parts[0][0] < self.grid_size[0] or not 0 <= self.snake.parts[0][1] < self.grid_size[1]:
            quit()
        # If the snake has collided with a fruit, spawn a new one and grow the snake
        if self.snake.parts[0] == self.fruit.position:
            self.fruit.position = self.generate_random_coords()
            self.snake.grow_snake()

    def draw_game(self):
        self.screen.fill((0, 0, 0))
        # draw score
        snake_ui.draw_text(f'{len(self.snake.parts)}', self.screen, (255,255,255), (10,10), 'arial.ttf', 46)
        for part in self.snake.parts:
            pygame.draw.rect(self.screen, self.snake.color, pygame.Rect(part[0] * 16, part[1] * 16, 16, 16))
        pygame.draw.rect(self.screen, self.fruit.color, pygame.Rect(self.fruit.position[0] * 16, self.fruit.position[1] * 16, 16, 16))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
