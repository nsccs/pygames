import pygame
import time
from enum import Enum
import random
from typing import Tuple


SCREEN_SIZE = 1000

# grid size is height and width of grid
GRID_LEN = 50
GRID_LAST = GRID_LEN - 1

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
        (self.x, self.y) = location
        self.living_neighbors = 0
        x,y = self.x, self.y
        # calculate neighbor position at init
        ul_field = (-1, -1)
        if x - 1 < 0 and y - 1 < 0:
            ul_field = (GRID_LAST, GRID_LAST)
        elif x - 1 < 0 and y - 1 >= 0:
            ul_field = (GRID_LAST, y - 1)
        elif x - 1 >= 0 and y - 1 < 0:
            ul_field = (x - 1, GRID_LAST)
        else:
            ul_field = (x - 1, y - 1)

        ur_field = (-1, -1)
        if x + 1 > GRID_LAST and y - 1 < 0:
            ur_field = (0,GRID_LAST)
        elif x + 1 > GRID_LAST and y - 1 >= 0:
            ur_field = (0, y - 1)
        elif x + 1 <= GRID_LAST and y - 1 < 0 :
            ur_field = (x + 1, GRID_LAST)
        else:
            ur_field = (x + 1, y - 1)

        bl_field = (-1, -1)
        if x - 1 < 0 and y + 1 > GRID_LAST:
            bl_field = (GRID_LAST, 0)
        elif x - 1 < 0 and y + 1 <= GRID_LAST:
            bl_field = (GRID_LAST, y + 1)
        elif x - 1 >= 0 and y + 1 > GRID_LAST:
            bl_field = (x - 1, 0)
        else:
            bl_field = (x - 1, y + 1)

        br_field = (-1, -1)
        if x + 1 > GRID_LAST and y + 1 > GRID_LAST:
            br_field = (0, 0)
        elif x + 1 > GRID_LAST and y + 1 <= GRID_LAST:
            br_field = (0, y + 1)
        elif x + 1 <= GRID_LAST and y + 1 > GRID_LAST:
            br_field = (x + 1, 0)
        else:
            br_field = (x + 1, y + 1)

        self.neighbors = [
            ul_field,
            (0, y) if x + 1 > GRID_LAST else (x + 1, y), # right
            ur_field,
            (x, 0) if y + 1 > GRID_LAST else (x, y + 1),  # bottom
            bl_field,
            (x, GRID_LAST) if y - 1 < 0 else (x, y - 1),  # top
            br_field,
            (GRID_LAST, y) if x - 1 < 0 else (x - 1, y)  # left
        ]
        t = SCREEN_SIZE/GRID_LEN
        self.is_alive = False
        self.rect = pygame.Rect(self.x * t, self.y * t, t, t)
        Cell.instances[location] = self

    def update(self):
        if (not self.is_alive) and self.living_neighbors == 3:
            Cell.changing.append((self, OperationFlag.REVIVE))
        elif self.is_alive and (self.living_neighbors < 2 or self.living_neighbors > 3) :
            Cell.changing.append((self, OperationFlag.KILL))

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
            #Cell.instances[n].living_neighbors -= 1
            self.is_alive = False

    def set_alive(self):
        Cell.changing.append((self, OperationFlag.REVIVE))

    def revive(self):
        if not self.is_alive:
            for n in self.neighbors:
                Cell.instances[n].living_neighbors += 1
            self.is_alive = True

    def draw(self, screen): 
        color = 0xffffff if self.is_alive else 0x000000
        if not self.is_alive:
            pygame.draw.rect(screen, color, self.rect)
            #screen.blit(pygame.font.SysFont('Arial', 25).render(f"{self.living_neighbors}", True, (255,255,255)), (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, color, self.rect)
            #screen.blit(pygame.font.SysFont('Arial', 25).render(f"{self.living_neighbors}", True, (0,0,0)), (self.rect.x, self.rect.y))
        return self.rect
        #pygame.display.update(self.rect)

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
        spaceship = [(34, 20), (37, 20), (38, 20), (45, 20), (48, 20), (49, 20), (50, 20), (26, 21), (30, 21), (31, 21), (32, 21), (33, 21), (35, 21), (36, 21), (37, 21), (38, 21), (39, 21), (40, 21), (45, 21), (48, 21), (49, 21), (50, 21), (22, 22), (23, 22), (24, 22), (25, 22), (26, 22), (31, 22), (36, 22), (41, 22), (42, 22), (43, 22), (21, 23), (28, 23), (29, 23), (31, 23), (38, 23), (39, 23), (41, 23), (42, 23), (43, 23), (46, 23), (48, 23), (49, 23), (50, 23), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (28, 24), (29, 24), (30, 24), (39, 24), (40, 24), (41, 24), (42, 24), (46, 24), (48, 24), (49, 24), (50, 24), (26, 25), (29, 25), (44, 25), (29, 26), (30, 26), (41, 26), (42, 26), (44, 26), (45, 26), (29, 27), (30, 27), (41, 27), (42, 27), (44, 27), (45, 27), (26, 28), (29, 28), (44, 28), (22, 29), (23, 29), (24, 29), (25, 29), (26, 29), (28, 29), (29, 29), (30, 29), (39, 29), (40, 29), (41, 29), (42, 29), (46, 29), (48, 29), (49, 29), (50, 29), (21, 30), (28, 30), (29, 30), (31, 30), (38, 30), (39, 30), (41, 30), (42, 30), (43, 30), (46, 30), (48, 30), (49, 30), (50, 30), (22, 31), (23, 31), (24, 31), (25, 31), (26, 31), (31, 31), (36, 31), (41, 31), (42, 31), (43, 31), (26, 32), (30, 32), (31, 32), (32, 32), (33, 32), (35, 32), (36, 32), (37, 32), (38, 32), (39, 32), (40, 32), (45, 32), (48, 32), (49, 32), (50, 32), (34, 33), (37, 33), (38, 33), (45, 33), (48, 33), (49, 33), (50, 33)]
        infinit = [(7, 0), (5, 1), (7, 1), (8, 1), (5, 2), (7, 2), (5, 3), (3, 4), (1, 5), (3, 5)]
        time_bomb = [(2, 0), (14, 0), (15, 0), (1, 1), (3, 1), (8, 1), (15, 1), (8, 2), (13, 2), (3, 3), (6, 3), (10, 3), (13, 3), (3, 4), (4, 4), (11, 4), (4, 5)]
        # nested loop generates location, initializes a cell, and inserts it in the dict
        for y in range(GRID_LEN):
            for x in range(GRID_LEN):
                Cell((x, y))
        
        # puts a glider on the grid
        for cell in spaceship:
            (x,y) = cell
            Cell.instances[(x + int(GRID_LEN/3), y + int(GRID_LEN/3))].set_alive()
        
    def run(self) -> None:
        """Main loop of game.

        Calls functions responsible for running game logic and drawing graphics every frame.
        """
        clock = pygame.time.Clock()
        while True:
            self.process_game_logic()
            self.draw_game_elements()
            #time.sleep(0.05)
            clock.tick()
            print(clock.get_fps())

    def process_game_logic(self):
        """Function for updating game logic every frame."""
        for cell in Cell.instances.values():
            cell.update()
        Cell.advance_generation()
        
        #file = open("log.txt", 'w')
        #for loc, cell in Cell.instances.items():
        #    file.write(f"CELL: {loc}:{cell.is_alive}: {cell.neighbors}:{cell.living_neighbors}\n")

    def draw_game_elements(self):
        updates = []
        """Method to draw to pygame screen every frame"""
        while len(Cell.changing) > 0:
            cell, _ = Cell.changing.pop(0)
            updates.append(cell.draw(self.screen))
        pygame.display.update(updates)

    def handle_input(self):
        pass

if __name__ == "__main__":
    game = Game()
    #input()
    game.run()
