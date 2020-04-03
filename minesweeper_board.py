import numpy as np
import random
#************************************************************************************************************************
#creating Minesweeper game board
"""grid = []
dim = int(input("Enter the dimension of the game: "))
num_mines = int(input("Enter the number of mines: "))
cells = [(i, j) for i in range(0, dim) for j in range(0, dim)]
sampling = random.sample(cells, num_mines) #cells in which mines are placed
for row in range(dim):
    grid.append([])
    for column in range(dim):
        if (row, column) in sampling:
            grid[row].append(1)
        else:
            grid[row].append(0)"""
#print(grid)
#************************************************************************************************************************

#************************************************************************************************************************
#creating Cell class
class Cell():
    def __init__(self, row, column, mine, revealed):
        self.row = row
        self.column = column
        self.mine = mine #to store whether it has a mine
        self.revealed = revealed #to store whether it has been revealed by the agent
        self.surrounding = 0 #to store how many surrounding mines there are

    def __eq__(self, other):
        return (self.row == other.row and self.column == other.column and self.mine == other.mine)
#************************************************************************************************************************




#************************************************************************************************************************
#global functions
def in_range(row, column, dim):
    return (row >= 0 and row < dim and column >= 0 and column < dim)

def neighbors(row, column, dim): #to return the adjacent cells
    return [tup for tup in [(row-1, column-1), (row-1, column), (row-1, column+1), (row, column-1), (row, column+1), (row+1, column-1), (row+1, column), (row+1, column+1)] if in_range(tup[0], tup[1], dim)]
#************************************************************************************************************************




#************************************************************************************************************************
#creating environment class for gameboard
class Agent():

    def __init__(self, dim, num_mines):
        self.gameboard = []
        self.dim = dim
        self.num_mines = num_mines
        self.unvisited = []
        self.visited = []
        cells = [(i, j) for i in range(0, self.dim) for j in range(0, self.dim)]
        sampling = random.sample(cells, num_mines) #cells in which mines are placed
        for row in range(self.dim):
            self.gameboard.append([])
            for column in range(self.dim):
                if (row, column) in sampling:
                    self.gameboard[row].append(Cell(row, column, True, False))
                else:
                    self.gameboard[row].append(Cell(row, column, False, False))

    def simple_solver():

    def csp_solver():




m = Agent(10, 15)
#print(m.gameboard)
l = neighbors(2,3, 10)
print(l)
