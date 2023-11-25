import pygame
import random 

grid_size = (32,32)
square_size = 16

screen_w = grid_size[0] * square_size
screen_h = grid_size[1] * square_size

starting_length = 3
snake_speed = 20

SNAKE_COLOR = (255,255,255)
BACKGROUND_COLOR = (0,0,0)
FOOD_COLOR = (255,0,0)

class Snake:
    def __init__(self, pos, direction, starting_length):
        self.pos = pos
        self.parts = [pos]

        #how many bodyparts it can grow
        #usualy only 0 or 1
        self.grow_count = starting_length
        self.direction = direction
        
    def update_snake(self):
        tail = self.parts[-1]
        
        #Updating the bodyparts
        partcopy = self.parts.copy()
        for part in range(len(partcopy) - 1):
	        self.parts[part + 1] = partcopy[part]

        #Growing a new bodypart
        if self.grow_count > 0:
            self.parts.append(tail)
            self.grow_count -= 1

        head_pos = self.parts[0]
        head_pos = (head_pos[0] + self.direction[0], head_pos[1] + self.direction[1])
        self.parts[0] = head_pos

    def grow_snake(self):
        self.grow_count += 1


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        self.screen.fill(BACKGROUND_COLOR)
        
        self.fps = pygame.time.Clock()
        
        self.snake = Snake((16,16),(1,0), starting_length)
        self.fruit_pos = self.spawn_fruit()
    
    #Spawns food at a random position
    def spawn_fruit(self):
        fruit_x = random.randint(0, grid_size[0] - 1)
        fruit_y = random.randint(0, grid_size[1] - 1)
        return (fruit_x, fruit_y)

    def run(self):
        while True:
            self.fps.tick(snake_speed)
            self.get_input()
            self.update_game()
            self.draw_game()
    def get_input(self):
        newdir = self.snake.direction
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    newdir = (0,-1)
                if event.key == pygame.K_DOWN:
                    newdir = (0,1)
                if event.key == pygame.K_LEFT:
                    newdir = (-1,0)
                if event.key == pygame.K_RIGHT:
                    newdir = (1,0)
        #This part of the code is so that the player cant flip the snake
        if newdir[0] != 0:
            if newdir[0] != self.snake.direction[0] * -1:
                self.snake.direction = newdir
        else:
            if newdir[1] != self.snake.direction[1] * -1:
                self.snake.direction = newdir
    #Updates the position of the snake, and checks other things
    def update_game(self):
        self.snake.update_snake()
        #If the snake has collided with itself
        if self.snake.parts[0] in self.snake.parts[1:]:
            quit()
        #If the snake has collided with the wall
        if not 0 <= self.snake.parts[0][0] < grid_size[0] or not 0 <= self.snake.parts[0][1] < grid_size[1]:
            quit()
        #If the snake has collided with a fruit, spawn a new one and grow the snake
        if self.snake.parts[0] == self.fruit_pos:
            self.fruit_pos = self.spawn_fruit()
            self.snake.grow_snake()
    def draw_game(self):
        self.screen.fill((0, 0, 0))
        for part in self.snake.parts:
            pygame.draw.rect(self.screen, SNAKE_COLOR, pygame.Rect(part[0] * 16 , part[1] * 16, 16, 16))
        pygame.draw.rect(self.screen, FOOD_COLOR, pygame.Rect(self.fruit_pos[0] * 16 , self.fruit_pos[1] * 16, 16, 16))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
			