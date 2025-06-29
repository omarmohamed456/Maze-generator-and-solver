import sys #mainly to run the project from the cmd and to get the file path #may be removed 
import random

import time #used in visualization #usen to calculate time to find a solution
from input_window import *

width, height, maze_seed, delay = get_maze_parameters()

random.seed(maze_seed)

# Constants
N, S, E, W = 1, 2,  4, 8    #bit flags
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}


class Tree:
    def __init__(self): #when the obj is first initialized
        self.parent = None

    def root(self):
        return self.parent.root() if self.parent else self  #action  if condition  else action
 
    def connected(self, tree): #avoid cycles ##check if both are in the same set
        return self.root() == tree.root()

    def connect(self, tree): #join
        tree.root().parent = self


grid = [[0 for _ in range(width)] for _ in range(height)] #This is the maze itself, a 2D list holding bit flags to mark which walls are open for each cell.


sets = [[Tree() for _ in range(width)] for _ in range(height)] #This is a 2D array of Tree objects, one Tree per cell, used to track which cells are connected as the maze is carved.
##################################

edges = [] 
for y in range(height):
    for x in range(width):
        if y > 0:
            #to make an opening and an exis propaply i will need to edit here
            edges.append((x, y, N))
        if x > 0:
            edges.append((x, y, W))

random.shuffle(edges)



print("\033[2J", end='')  # Clear the screen


def carve_entrance_exit(grid, width, height):
        # Randomly select entrance and exit only once
        global start_cell 
        global end_cell
        start_c = random.randint(0, width - 1)
        end_c = random.randint(0, width - 1)

        # Carve entrance (top row, open to the north)
        grid[0][start_c] |= N

        # Carve exit (bottom row, open to the south)
        grid[height - 1][end_c] |= S

        start_cell = (start_c, 0)              # top row
        end_cell = (end_c, height - 1)         # bottom row

first = True  # Flag to mark first iteration


while edges:
    x, y, direction = edges.pop()

    nx, ny = x + DX[direction], y + DY[direction] #direction = N or W only

    set1, set2 = sets[y][x], sets[ny][nx]

    if not set1.connected(set2): 

        if first:
            
            carve_entrance_exit(grid, width, height)

            first = False  # So it doesn't happen again

        time.sleep(delay) #use the delay for visualization

        set1.connect(set2)
        grid[y][x] |= direction #this is a bitwise operator that adds the values of n w e s together if a cell have the value of 6 it means the E and S values 2 and 4 are added which tells the display function to remove the wall between these two cells visually  
        grid[ny][nx] |= OPPOSITE[direction] #this removes corresponding wall in the neighbour cell because if the cell on the west side of cell 1 is removed the east wall one cell 2 (one its left) should be removed 


# Show parameters
print(f"\nGenrated maze: \nPath:{sys.argv[0]} \nWidth: {width} \nHeight: {height} \nSeed: {maze_seed} \ndelay time: {delay} \n")
