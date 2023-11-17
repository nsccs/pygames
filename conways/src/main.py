#!python
import pygame
from enum import Enum


PRESETS = {
    "glider": [(5, 5), (6, 6), (6, 7), (5, 7), (4, 7)],
    "spaceship": [(34, 20), (37, 20), (38, 20), (45, 20), (48, 20), (49, 20), (50, 20), (26, 21), (30, 21), (31, 21), (32, 21), (33, 21), (35, 21), (36, 21), (37, 21), (38, 21), (39, 21), (40, 21), (45, 21), (48, 21), (49, 21), (50, 21), (22, 22), (23, 22), (24, 22), (25, 22), (26, 22), (31, 22), (36, 22), (41, 22), (42, 22), (43, 22), (21, 23), (28, 23), (29, 23), (31, 23), (38, 23), (39, 23), (41, 23), (42, 23), (43, 23), (46, 23), (48, 23), (49, 23), (50, 23), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (28, 24), (29, 24), (30, 24), (39, 24), (40, 24), (41, 24), (42, 24), (46, 24), (48, 24), (49, 24), (50, 24), (26, 25), (29, 25), (44, 25), (29, 26), (30, 26), (41, 26), (42, 26), (44, 26), (45, 26), (29, 27), (30, 27), (41, 27), (42, 27), (44, 27), (45, 27), (26, 28), (29, 28), (44, 28), (22, 29), (23, 29), (24, 29), (25, 29), (26, 29), (28, 29), (29, 29), (30, 29), (39, 29), (40, 29), (41, 29), (42, 29), (46, 29), (48, 29), (49, 29), (50, 29), (21, 30), (28, 30), (29, 30), (31, 30), (38, 30), (39, 30), (41, 30), (42, 30), (43, 30), (46, 30), (48, 30), (49, 30), (50, 30), (22, 31), (23, 31), (24, 31), (25, 31), (26, 31), (31, 31), (36, 31), (41, 31), (42, 31), (43, 31), (26, 32), (30, 32), (31, 32), (32, 32), (33, 32), (35, 32), (36, 32), (37, 32), (38, 32), (39, 32), (40, 32), (45, 32), (48, 32), (49, 32), (50, 32), (34, 33), (37, 33), (38, 33), (45, 33), (48, 33), (49, 33), (50, 33)],
    "infinite_growth": [(7, 0), (5, 1), (7, 1), (8, 1), (5, 2), (7, 2), (5, 3), (3, 4), (1, 5), (3, 5)],
    "time_bomb": [(2, 0), (14, 0), (15, 0), (1, 1), (3, 1), (8, 1), (15, 1), (8, 2), (13, 2), (3, 3), (6, 3), (10, 3), (13, 3), (3, 4), (4, 4), (11, 4), (4, 5)],
}


SCREEN_SIZE = 1000

# grid size is height and width of grid
GRID_LEN = 500
GRID_LAST = GRID_LEN - 1


class OperationFlag(Enum):
    """ Enum used when inserting references to cells into the list of changing
    cells every cycle
    """
    REVIVE = 0
    KILL = 1


class Cells(dict):
    """Collection of Cells"""
    __slots__ = 'changing', 'screen'

    def __init__(self, *arg, **kw):
        """Make a grid of cells the size of GRID_LEN"""
        super(Cells, self).__init__(*arg, **kw)
        self.changing = []
        for y in range(GRID_LEN):
            for x in range(GRID_LEN):
                loc = (x, y)
                self[loc] = self.cell(loc)

    def cell(self, *arg, **kw):
        """add cell to collection"""
        cell = Cell(*arg, **kw)
        return cell

    def load_preset(self, key, offsetx=0, offsety=0):
        """load an array of points to set alive"""
        try:
            for (x, y) in PRESETS[key]:
                self.set_alive((x + offsetx, y + offsety))
        except KeyError:
            print("KEYERROR: ", key)# maybe display error over game

    def advance_generation(self):
        """process changing cells"""
        for cell in self.values():
            result = cell.update()
            if result is not None:
                self.changing.append(result)

        for cell, op in self.changing:
            if op == OperationFlag.KILL:
                self.kill(cell)
            elif op == OperationFlag.REVIVE:
                self.revive(cell)

    def draw_cells(self, screen):
        """Draw changing cells"""
        updates = []
        while len(self.changing) > 0:
            cell, _ = self.changing.pop(0)
            updates.append(cell.draw(screen))
        return updates

    def kill(self, cell):
        """kill cell and decrement living neighbor count of neighbors"""
        if cell.is_alive:
            for loc in cell.neighbors:
                if self[loc].living_neighbors > 0:
                    self[loc].living_neighbors -= 1
            cell.is_alive = False

    def set_alive(self, loc):
        """set cell as alive. Used for manual enabling. Maybe useful or User Input."""
        self.changing.append((self[loc], OperationFlag.REVIVE))

    def revive(self, cell):
        """revive cell and increment living neighbor count of neighbors"""
        if not cell.is_alive:
            for loc in cell.neighbors:
                self[loc].living_neighbors += 1
            cell.is_alive = True


class Cell(object):
    """Simple class that defines a cell."""

    __slots__ = 'location', 'neighbors', 'living_neighbors', 'is_alive', 'rect'
    # location of cell and whether it is alive or dead

    def __init__(self, location):
        """cells are initialized with a location, their neighbors are located
        at this time
        """
        (x, y) = self.location = location

        # calculate neighbor positions
        ul_field = (x - 1, y - 1)
        if x - 1 < 0 and y - 1 < 0:
            ul_field = (GRID_LAST, GRID_LAST)
        elif x - 1 < 0 and y - 1 >= 0:
            ul_field = (GRID_LAST, y - 1)
        elif x - 1 >= 0 and y - 1 < 0:
            ul_field = (x - 1, GRID_LAST)

        ur_field = (x + 1, y - 1)
        if x + 1 > GRID_LAST and y - 1 < 0:
            ur_field = (0, GRID_LAST)
        elif x + 1 > GRID_LAST and y - 1 >= 0:
            ur_field = (0, y - 1)
        elif x + 1 <= GRID_LAST and y - 1 < 0:
            ur_field = (x + 1, GRID_LAST)

        bl_field = (x - 1, y + 1)
        if x - 1 < 0 and y + 1 > GRID_LAST:
            bl_field = (GRID_LAST, 0)
        elif x - 1 < 0 and y + 1 <= GRID_LAST:
            bl_field = (GRID_LAST, y + 1)
        elif x - 1 >= 0 and y + 1 > GRID_LAST:
            bl_field = (x - 1, 0)

        br_field = (x + 1, y + 1)
        if x + 1 > GRID_LAST and y + 1 > GRID_LAST:
            br_field = (0, 0)
        elif x + 1 > GRID_LAST and y + 1 <= GRID_LAST:
            br_field = (0, y + 1)
        elif x + 1 <= GRID_LAST and y + 1 > GRID_LAST:
            br_field = (x + 1, 0)

        right_field = (0, y) if x + 1 > GRID_LAST else (x + 1, y)
        bottom_field = (x, 0) if y + 1 > GRID_LAST else (x, y + 1)
        top_field = (x, GRID_LAST) if y - 1 < 0 else (x, y - 1)
        left_field = (GRID_LAST, y) if x - 1 < 0 else (x - 1, y)

        self.neighbors = [
            ul_field,
            right_field,
            ur_field,
            bottom_field,
            bl_field,
            top_field,
            br_field,
            left_field
        ]

        self.is_alive = False
        scale = SCREEN_SIZE/GRID_LEN
        self.rect = pygame.Rect(x * scale, y * scale, scale, scale)
        self.living_neighbors = 0

    def update(self):
        """Check cell against Game of life rules"""
        if (not self.is_alive) and self.living_neighbors == 3:
            return (self, OperationFlag.REVIVE)
        elif self.is_alive and (self.living_neighbors < 2 or self.living_neighbors > 3) :
            return (self, OperationFlag.KILL)

    def draw(self, screen):
        "draw self and return rect to be updated"
        color = 0xffffff if self.is_alive else 0x000000
        pygame.draw.rect(screen, color, self.rect)
        return self.rect


class Game:
    """ Game class handles the main loop and io."""

    # reference to initialized pygame screen
    __slots__ = 'screen', 'cells'

    def __init__(self, title: str = "NSCCSC Life Clone") -> None:
        # pygame setup
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        # Cells setup
        self.cells = Cells()
        self.cells.load_preset("time_bomb", 200)

    def run(self) -> None:
        """Main loop of game.

        Calls functions responsible for running game logic and drawing graphics every frame.
        """
        while True:
            self.process_game_logic()
            self.draw_game_elements()

    def process_game_logic(self):
        """Function for updating game logic every frame."""
        self.cells.advance_generation()

    def draw_game_elements(self):
        """Method to draw to pygame screen every frame"""
        updates = self.cells.draw_cells(self.screen)
        pygame.display.update(updates)

    def handle_input(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.run()
