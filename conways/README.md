# Conway's Game of Life

A clone of Life written in python and using pygame.

## Playing the game

Simply run `./src/main` to launch the current demo. If you want to see another demo you will have to edit line 189 of the script to a different key.


## The Rules

1. A cell can be either "alive" or "dead"
2. If a dead cell is surrounded by **three** living cells it is revived.
3. If a living cell has **one** or **zero** living neighbors it "dies of loneliness".
4. If a living cell has **four or more** living neighbors it "dies of overcrowding".

Every generation every cell is checked against these condition to determine their state in the next generation.

## How it works

### Cells

Cells are simply alive or dead, know where their neighbors are, and how to direct their updates based on the number of living neighbors they have. They can also draw themselves. Living neighbors are calculated on a revive or death even for all neighbors of the changing cell. The `Cells` class is responsible for doing group operations on the cell and contains all the cells for a grid.

### The "universe" of Life is an infinite grid of cells.

Because we have to represent the grid with a fixed size in code we have to treat the grid as torroidal. To do so we simply wrap around the grid if the cell is on the border.

## Things To Work On:
To me these are the things that would take this project up a notch.
### UI
- the ability to control generation speed
- ability to set cells alive on click
- GUI like tkinter
- scrolling/zooming
### Features
- Stepping through generations
- play/pause
- import/export presets
- library of presets
- real time grid resizing



