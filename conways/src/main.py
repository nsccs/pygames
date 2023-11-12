import pygame
import time
from os import system
from enum import Enum

# grid size is height and width of grid
GRID_SIZE = 20

# chars for printing game to console. change to something fun if you want!
ALIVE = '⬜'
DEAD = '⬛'

class OperationFlag(Enum):
    """ Enum used when inserting references to cells into the list of changing cells every cycle"""
    REVIVE = 0 
    KILL = 1

# All cells belonging to grid. Key is the location.    
cells = {}

def check_on_neighbors(location) -> int:
    """A function that counts how many of a cell's neighbors are alive.

    Takes the location of the cell and returns the number of living cells.
    
    Wrapping is performed if any neighbors are beyond the grid's boundaries.
    """

    living = 0
    (x,y) = location

    # need to check cases where any neighbor might be on the other side of the grid
    match [x - 1 < 0, x + 1 >= GRID_SIZE, y - 1 < 0, y + 1 >= GRID_SIZE]:
        
        # left top corner case
        case [True, False, True, False]:
            if cells[GRID_SIZE - 1, GRID_SIZE - 1].is_alive: living += 1
            if cells[GRID_SIZE - 1, y].is_alive: living += 1
            if cells[GRID_SIZE - 1, y + 1].is_alive: living += 1
            if cells[x + 1, GRID_SIZE - 1].is_alive: living += 1
            if cells[x + 1, y].is_alive: living += 1
            if cells[x + 1, y + 1].is_alive: living += 1
            if cells[x, GRID_SIZE - 1].is_alive: living += 1
            if cells[x, y + 1].is_alive: living += 1
        
        # left bottom corner case
        case [True, False, False, True]:
            if cells[GRID_SIZE - 1, y - 1].is_alive: living += 1
            if cells[GRID_SIZE - 1, y].is_alive: living += 1
            if cells[GRID_SIZE - 1, 0].is_alive: living += 1
            if cells[x + 1, y-1].is_alive: living += 1
            if cells[x + 1, y].is_alive: living += 1
            if cells[x + 1, 0].is_alive: living += 1
            if cells[x, y - 1].is_alive: living += 1
            if cells[x, 0].is_alive: living += 1
        
        # right bottom corner case
        case [False, True, False, True]:
            if cells[x - 1, y - 1].is_alive: living += 1
            if cells[x - 1, y].is_alive: living += 1
            if cells[x - 1, 0].is_alive: living += 1
            if cells[0, y - 1].is_alive: living += 1
            if cells[0, y].is_alive: living += 1
            if cells[0, 0].is_alive: living += 1
            if cells[x, y - 1].is_alive: living += 1
            if cells[x, 0].is_alive: living += 1


        # right top corner case
        case [False, True, True, False]:
            if cells[x - 1, GRID_SIZE - 1].is_alive: living += 1
            if cells[x - 1, y].is_alive: living += 1
            if cells[x - 1, y + 1].is_alive: living += 1
            if cells[0, GRID_SIZE - 1].is_alive: living += 1
            if cells[0, y].is_alive: living += 1
            if cells[0, y + 1].is_alive: living += 1
            if cells[x, GRID_SIZE - 1].is_alive: living += 1
            if cells[x, y + 1].is_alive: living += 1

        # left border case
        case [True, False, False, False]:
            if cells[GRID_SIZE - 1, y - 1].is_alive: living += 1
            if cells[GRID_SIZE - 1, y].is_alive: living += 1
            if cells[GRID_SIZE - 1, y + 1].is_alive: living += 1
            if cells[x + 1, y - 1].is_alive: living += 1
            if cells[x + 1, y].is_alive: living += 1
            if cells[x + 1, y + 1].is_alive: living += 1
            if cells[x, y - 1].is_alive: living += 1
            if cells[x, y + 1].is_alive: living += 1
        
        # right border case
        case [False, True, False, False]:
            if cells[x - 1, y - 1].is_alive: living += 1
            if cells[x - 1, y].is_alive: living += 1
            if cells[x - 1, y + 1].is_alive: living += 1
            if cells[0, y - 1].is_alive: living += 1
            if cells[0, y].is_alive: living += 1
            if cells[0, y + 1].is_alive: living += 1
            if cells[x, y - 1].is_alive: living += 1
            if cells[x, y + 1].is_alive: living += 1

        # bottom border case
        case [False, False, False, True]:
            if cells[x - 1, y - 1].is_alive: living += 1
            if cells[x - 1, y].is_alive: living += 1
            if cells[x - 1, 0].is_alive: living += 1
            if cells[x + 1, y - 1].is_alive: living += 1
            if cells[x + 1, y].is_alive: living += 1
            if cells[x + 1, 0].is_alive: living += 1
            if cells[x, y - 1].is_alive: living += 1
            if cells[x, 0].is_alive: living += 1
        
        # top border case
        case [False, False, True, False]:
            if cells[x - 1, GRID_SIZE - 1].is_alive: living += 1
            if cells[x - 1, y].is_alive: living += 1
            if cells[x - 1, y + 1].is_alive: living += 1
            if cells[x + 1, GRID_SIZE - 1].is_alive: living += 1
            if cells[x + 1, y].is_alive: living += 1
            if cells[x + 1, y + 1].is_alive: living += 1
            if cells[x, GRID_SIZE - 1].is_alive: living += 1
            if cells[x, y + 1].is_alive: living += 1
        
        # standard case
        case [False, False, False, False]:
            if cells[x - 1, y - 1].is_alive: living += 1
            if cells[x - 1, y].is_alive: living += 1
            if cells[x - 1, y + 1].is_alive: living += 1
            if cells[x + 1, y - 1].is_alive: living += 1
            if cells[x + 1, y].is_alive: living += 1
            if cells[x + 1, y + 1].is_alive: living += 1
            if cells[x, y - 1].is_alive: living += 1
            if cells[x, y + 1].is_alive: living += 1

    return living

class Cell:
    """Simple class that defines a cell.
    
    Initialized with the location in the grid. This is desirable because it 
    removes the need for any underlying 2d array for the grid as we can use location
    as keys in a dictonary.
    """
    
    # location of cell and whether it is alive or dead
    __slots__= 'location', 'is_alive'

    def __init__(self, location) -> None:
        self.location = location
        self.is_alive = False
            
 
class Game:
    """ Game class handles the main loop and io."""

    # reference to initialized pygame screen
    __slots__ = 'screen'

    def __init__(self, title: str = "NSCCSC Life Clone") -> None:
        pygame.init()
        pygame.display.set_caption(title)

        # nested loop generates location, initializes a cell, and inserts it in the dict
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cells[(x, y)] = Cell((x, y))

        self.screen = pygame.display.set_mode((800, 600))

        # uncomment following code to put a glider on the grid
        # useful for running game without input
        #
        # cells[(5,5)].is_alive = True
        # cells[(6,6)].is_alive = True
        # cells[(6,7)].is_alive = True
        # cells[(5,7)].is_alive = True
        # cells[(4,7)].is_alive = True
       

    def run(self) -> None:
        """Main loop of game.
            
        Calls functions responsible for running game logic and drawing graphics every frame.
        """
        while True:
            self.process_game_logic()
            self.draw_game_elements()

    def process_game_logic(self):
        """Function for updating game logic every frame."""

        changing = [] # references to all cells changing this frame and the outcome

        # for every cell check its neighbors and detirmine if its changing
        for cell in cells.values():
            living = check_on_neighbors(cell.location)
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
        for y in range(GRID_SIZE):
            print("", end="")
            for x in range(GRID_SIZE):
                cell = cells[(x,y)]
                if cell.is_alive:
                    print(ALIVE, end="")
                else: 
                    print(DEAD, end="")
            print()


if __name__ == "__main__":
    game = Game()
    game.run()

    
    # Fake game loop for printing game to console
    #while True:
    #    game.draw_in_console()
    #    game.process_game_logic()
    #    time.sleep(0.1) # change to adjust print speed
