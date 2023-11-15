# Conway's Game of Life

A clone of Life written in python and using pygame.

## Playing the game



## The Rules

1. A cell can be either "alive" or "dead"
2. If a dead cell is surrounded by **three** living cells it is revived.
3. If a living cell has **one** or **zero** living neighbors it "dies of loneliness".
4. If a living cell has **four or more** living neighbors it "dies of overcrowding".

Every generation every cell is checked against these condition to determine their state in the next generation.

## How it works

### Cells

Cells are simply alive or dead and can be asked for the location of the neighbors with which they share a side (left, right, up, down).

### Egocentric approach

Because the cells can report their neighbors location we can take an approach where every cell's state is based on it's perspective of it's neighbors. In simpler terms, we can simply ask a cell and its imediate neighbors to tell us the sum of living cells in the field surrounding a location.

### The "universe" of Life is an infinite grid of cells.

Because we have to represent the grid with a fixed size in code we have to treat the grid as torroidal. To do so we simply wrap around the grid if the cell is on the border.



