import pygame
import time
from os import system
import sys
from enum import Enum
from typing import Tuple


SCREEN_SIZE = 1000

# grid size is height and width of grid
GRID_LEN = 200
GRID_LAST = GRID_LEN - 1

# chars for printing game to console. change to something fun if you want!
ALIVE = '⬜'
DEAD = '⬛'


class OperationFlag(Enum):
    """ Enum used when inserting references to cells into the list of changing 
    cells every cycle
    """
    REVIVE = 0
    KILL = 1


class Cell:
    """Simple class that defines a cell.

    Initialized with the location in the grid. This is desirable because it 
    removes the need for any underlying 2d array for the grid as we can use location
    as keys in a dictonary.
    """

    # location of cell and whether it is alive or dead
    __slots__ = 'x', 'y', 'is_alive', 'rect', 'living_neighbors', 'neighbors'
    
    instances = {}
    changing = []

    def __init__(self, location: Tuple[int, int]) -> None:
        (self.x, self.y)= (x,y) = location
        self.living_neighbors = 0

        # calculate neighbor position at init
        ul_field = (-1, -1)
        if x - 1 and y - 1 < 0:
            ul_field = (GRID_LAST, GRID_LAST)
        elif x - 1 < 0 and y - 1 > 0:
            ul_field = (GRID_LAST, y - 1)
        else:
            ul_field = (x - 1, y - 1)

        self.neighbors = [
            ul_field,
            (0, y) if x + 1 > GRID_LAST else (x + 1, y),
            (self.x + 1, self.y + 1) if self.x + 1 <= GRID_LAST and self.y + 1 <= GRID_LAST else (0, 0), # bottom right corner
            (x, 0) if y + 1 > GRID_LAST else (x, y + 1),  # bottom
            ((GRID_LAST, 0) if x - 1 < 0 and y + 1 > GRID_LAST else (x - 1, y + 1)), # bottom left corner
            (x, GRID_LAST) if y - 1 < 0 else (x, y - 1),  # top
            (GRID_LAST, y) if x - 1 < 0 else (x - 1, y)  # left
        ]
        print("(",self.x,",",self.y,")", self.neighbors)
        self.is_alive = False
        t = SCREEN_SIZE/GRID_LEN
        self.rect = pygame.Rect(self.x * t, self.y * t, t, t)
        Cell.instances[location] = self

    def update(self):
        if self.is_alive and not 2 <= self.living_neighbors < 4:
            Cell.changing.append((self, OperationFlag.KILL))
        elif not self.is_alive and self.living_neighbors == 3:
            Cell.changing.append((self, OperationFlag.REVIVE))

    def advance_generation():
        for cell, op in Cell.changing:
            if op == OperationFlag.KILL:
                cell.kill()

            elif op == OperationFlag.REVIVE:
                cell.revive()

    def kill(self):
        if self.is_alive:
            for n in self.neighbors:
                cell = Cell.instances[n]
                if cell.living_neighbors > 0:
                    cell.living_neighbors -= 1
            self.is_alive = False

    def revive(self):
        if not self.is_alive:
            for n in self.neighbors:
                Cell.instances[n].living_neighbors += 1
            self.is_alive = True

    def draw(self, screen):
        color = 0xffffff if self.is_alive else 0x000000
        pygame.draw.rect(screen, color, self.rect)

    def location(self):
        return (self.x, self.y)

    def get_cells():
        return Cell.instances

    def to_string(self):
        return "{loc}: {living}".format(loc = self.location(), living = self.living_neighbors)


class Game:
    """ Game class handles the main loop and io."""

    # reference to initialized pygame screen
    __slots__ = 'screen', 'cells'

    def __init__(self, title: str = "NSCCSC Life Clone") -> None:
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

        glider = [(5, 5), (6, 6), (6, 7), (5, 7), (4, 7)]

        spaceship = [(113, 100), (116, 100), (117, 100), (124, 100), (127, 100), (128, 100), (129, 100), (105, 101), (109, 101), (110, 101), (111, 101), (112, 101), (114, 101), (115, 101), (116, 101), (117, 101), (118, 101), (119, 101), (124, 101), (127, 101), (128, 101), (129, 101), (101, 102), (102, 102), (103, 102), (104, 102), (105, 102), (110, 102), (115, 102), (120, 102), (121, 102), (122, 102), (100, 103), (107, 103), (108, 103), (110, 103), (117, 103), (118, 103), (120, 103), (121, 103), (122, 103), (125, 103), (127, 103), (128, 103), (129, 103), (101, 104), (102, 104), (103, 104), (104, 104), (105, 104), (107, 104), (108, 104), (109, 104), (118, 104), (119, 104), (120, 104), (121, 104), (125, 104), (127, 104), (128, 104), (129, 104), (105, 105), (108, 105), (123, 105), (108, 106), (109, 106), (120, 106), (121, 106), (123, 106), (124, 106), (108, 107), (109, 107), (120, 107), (121, 107), (123, 107), (124, 107), (105, 108), (108, 108), (123, 108), (101, 109), (102, 109), (103, 109), (104, 109), (105, 109), (107, 109), (108, 109), (109, 109), (118, 109), (119, 109), (120, 109), (121, 109), (125, 109), (127, 109), (128, 109), (129, 109), (100, 110), (107, 110), (108, 110), (110, 110), (117, 110), (118, 110), (120, 110), (121, 110), (122, 110), (125, 110), (127, 110), (128, 110), (129, 110), (101, 111), (102, 111), (103, 111), (104, 111), (105, 111), (110, 111), (115, 111), (120, 111), (121, 111), (122, 111), (105, 112), (109, 112), (110, 112), (111, 112), (112, 112), (114, 112), (115, 112), (116, 112), (117, 112), (118, 112), (119, 112), (124, 112), (127, 112), (128, 112), (129, 112), (113, 113), (116, 113), (117, 113), (124, 113), (127, 113), (128, 113), (129, 113)]

        # nested loop generates location, initializes a cell, and inserts it in the dict
        for y in range(GRID_LEN):
            for x in range(GRID_LEN):
                Cell((x, y))
        
        # puts a glider on the grid
        for cell in spaceship:
            Cell.instances[cell].revive()


    def run(self) -> None:
        """Main loop of game.

        Calls functions responsible for running game logic and drawing graphics every frame.
        """
        while True:
            self.draw_game_elements()
            self.process_game_logic()
            input()

    def process_game_logic(self):
        """Function for updating game logic every frame."""

        for cell in Cell.instances.values():
            cell.update()
        Cell.advance_generation()

    def draw_game_elements(self):
        """Method to draw to pygame screen every frame"""
        while len(Cell.changing) > 0:
            cell, _ = Cell.changing.pop(0)
            cell.draw(self.screen)
            pygame.display.update(cell.rect)

    def handle_input(self):
        pass

if __name__ == "__main__":
    game = Game()
    game.run()
