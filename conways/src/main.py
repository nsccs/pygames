import pygame
import time
from os import system
from enum import Enum
from typing import Tuple

# grid size is height and width of grid
GRID_LEN = 20
GRID_LAST = GRID_LEN - 1 

# chars for printing game to console. change to something fun if you want!
ALIVE = '⬜'
DEAD = '⬛'

class OperationFlag(Enum):
    """ Enum used when inserting references to cells into the list of changing cells every cycle"""
    REVIVE = 0 
    KILL = 1

class Cell:
    """Simple class that defines a cell.
    
    Initialized with the location in the grid. This is desirable because it 
    removes the need for any underlying 2d array for the grid as we can use location
    as keys in a dictonary.
    """
    
    # location of cell and whether it is alive or dead
    __slots__= 'x', 'y', 'is_alive'

    def __init__(self, location: Tuple[int, int]) -> None:
        (self.x, self.y) = location
        self.is_alive = False

    def location(self):
        return (self.x, self.y)

    def get_left_neighbor_loc(self) -> Tuple[int, int]:
        if self.x - 1 < 0:
            return (GRID_LAST, self.y)
        else:
            return (self.x - 1, self.y)
    
    def get_right_neighbor_loc(self) -> Tuple[int, int]:
        if self.x + 1 > GRID_LAST:
            return (0, self.y)
        else:
            return (self.x + 1, self.y)

    def get_top_neighbor_loc(self) -> Tuple[int, int]:
        if self.y - 1 < 0:
            return (self.x, GRID_LAST)
        else:
            return (self.x, self.y - 1)
    
    def get_bottom_neighbor_loc(self) -> Tuple[int, int]:
        if self.y + 1 > GRID_LAST:
            return (self.x, 0)
        else:
            return (self.x, self.y + 1)


            
 
class Game:
    """ Game class handles the main loop and io."""

    # reference to initialized pygame screen
    __slots__ = 'screen'
    cells = {}

    def __init__(self, title: str = "NSCCSC Life Clone") -> None:
        pygame.init()
        pygame.display.set_caption(title)

        # nested loop generates location, initializes a cell, and inserts it in the dict
        for y in range(GRID_LEN):
            for x in range(GRID_LEN):
                self.cells[(x, y)] = Cell((x, y))

        #self.screen = pygame.display.set_mode((800, 600))

        # uncomment following code to put a glider on the grid
        # useful for running game without input
        #
        #self.cells[(5,5)].is_alive = True
        #self.cells[(6,6)].is_alive = True
        #self.cells[(6,7)].is_alive = True
        #self.cells[(5,7)].is_alive = True
        #self.cells[(4,7)].is_alive = True

    def run(self) -> None:
        """Main loop of game.
            
        Calls functions responsible for running game logic and drawing graphics every frame.
        """
        while True:
            self.process_game_logic()
            self.draw_game_elements()

    def check_cell_neighbors(self, cell: Cell) -> int:
        """ Checks how many neighbors are alive """
        living = 0
        
        top_cell = self.cells[cell.get_top_neighbor_loc()]       
        top_left_cell = self.cells[top_cell.get_left_neighbor_loc()]
        top_right_cell = self.cells[top_cell.get_right_neighbor_loc()]
        bottom_cell = self.cells[cell.get_bottom_neighbor_loc()]
        bottom_left_cell = self.cells[bottom_cell.get_left_neighbor_loc()]
        bottom_right_cell = self.cells[bottom_cell.get_right_neighbor_loc()]
        left_cell = self.cells[cell.get_left_neighbor_loc()]
        right_cell = self.cells[cell.get_right_neighbor_loc()]
        

        living = len(list(filter(lambda x: x.is_alive, [
            top_cell, 
            top_left_cell,
            top_right_cell,
            bottom_cell,
            bottom_left_cell,
            bottom_right_cell,
            left_cell,
            right_cell
        ])))

        return living
        

    def process_game_logic(self):
        """Function for updating game logic every frame."""

        changing = [] # references to all cells changing this frame and the outcome

        # for every cell check its neighbors and detirmine if its changing
        for cell in self.cells.values():
            living = self.check_cell_neighbors(cell)
            if not (1 < living < 4): # death condition
                changing.append((cell, OperationFlag.KILL))
            elif living == 3: # revive condition
                changing.append((cell, OperationFlag.REVIVE))
        
        # for every changing cell apply change
        for cell in changing:
            (cell, op) = cell
            match op:
                case OperationFlag.KILL:
                    cell.is_alive = False
                case OperationFlag.REVIVE:
                    cell.is_alive = True
    
    def draw_game_elements(self):
        """Method to draw to pygame screen every frame"""
        pass

    def draw_in_console(self):
        """Method to see game in console"""
        system('clear')
        for y in range(GRID_LEN):
            print("", end="")
            for x in range(GRID_LEN):
                cell = self.cells[(x,y)]
                if cell.is_alive:
                    print(ALIVE, end="")
                else: 
                    print(DEAD, end="")
            print()



if __name__ == "__main__":
    game = Game()
    #game.run()

    
    # Fake game loop for printing game to console
    while True:
        game.draw_in_console()
        game.process_game_logic()
        time.sleep(0.1)
