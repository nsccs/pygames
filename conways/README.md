# Conway's Game of Life

A clone of Life written in python and using pygame.

## The Rules

1. A cell can be either "alive" or "dead"
2. If a dead cell is surrounded by **three** living cells it is revived.
3. If a living cell has **one** or **zero** living neighbors it "dies of loneliness".
4. If a living cell has **four or more** living neighbors it "dies of overcrowding".

Every generation every cell is checked against these condition to determine their state in the next generation.

## How it works

### Every cell is represented by the `Cell` class.

The class stores information about the cell's state and location. It also defines the capability to locate its neighbors that share a side with it (left, right, up, down).

### The games grid is a Torroidal Graph



## A Little Bit of History

<p>Life is a facinating cellular automaton created in 1970 by the mathematician John Horton Conway. In an interview with the YouTube channel</p>