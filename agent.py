import numpy as np
import random

class Agent:
    def __init__(self, env, total_mines):
        self.env = env
        self.total_mines = total_mines

    def start(self):
        # open first cell
        self.env[0][0].is_open = True
        # if the cell is a mine
        if self.env[0][0].mine_value == 1:
            self.env[0][0].is_safe = 0
            #self.safe_neighbors = -1  # num safe squares identified around it
            #self.mine_neighbors = -1  # num mines identified around it
            #self.hidden_neighbors = -1  # num hidden neighbors around it
        # if the cell is safe
        return self.env

    def print_env(self):
        dim = len(self.env)
        for row in range(dim):
            for col in range(dim):
                if not self.env[row][col].is_open:
                    print('X', end='  ')
                else:
                    if self.env[row][col].mine_value == 0:
                        print(str(self.env[row][col].value), end='  ')
                    if self.env[row][col].mine_value == 1:
                        if self.env[row][col].is_flagged:
                            print('F', end='  ')
                        else:
                            print('M', end='  ')
            print('')

    def naive_solver(self):
        # init vars
        num_visited_mines = 0
        num_flagged_mines = 0
        dim = len(self.env)
        # generate list of cell position options
        cell_options = [(i, j) for i in np.arange(0,dim) for j in np.arange(0,dim)]

        while num_visited_mines < self.total_mines:
            # randomly select a cell
            if len(cell_options) == 0: # if cell options is empty
                break
            pos = random.choice(cell_options)
            cell_options.remove(pos)  # remove from list of options
            cell = self.env[pos[0]][pos[1]]

            # open cell
            cell.is_open = True

            # if cell is not a mine
            if cell.mine_value == 0:
                # mark cell as safe
                cell.is_safe = 1

                # if cell value can provide more clues
                if cell.value == 0:  # when value is zero
                    for n in self.get_neighbors(pos[0], pos[1]):  # all neighbors are safe
                        n[0].is_safe = 1
                        n[0].is_open = True
                        continue;

                # gather info from nearby cells
                self.gather_info(pos[0], pos[1])

                if (cell.value - cell.mine_neighbors) == cell.hidden_neighbors:
                    for n in self.get_neighbors(pos[0], pos[1]):
                        if not n[0].is_open:
                            n[0].mine_value = 1
                            n[0].is_safe = 0
                            n[0].is_open = True
                            n[0].is_flagged = True
                            num_visited_mines += 1
                            num_flagged_mines += 1

                if ((8-cell.value) - cell.safe_neighbors) == cell.hidden_neighbors:
                    for n in self.get_neighbors(pos[0], pos[1]):
                        if n[0].is_open == False:
                            n[0].is_safe = 1
                            n[0].is_open = True



            # if cell is mine (and you exploded a mine)
            elif cell.mine_value == 1:
                num_visited_mines += 1
                cell.is_safe = 0  # indicate cell is unsafe

            #print(cell)
            print(pos[0], pos[1])
            self.print_env()
            print('-------')

            # remove opened cells from options
            for row in range(dim):
                for col in range(dim):
                    if self.env[row][col].is_open and cell_options.__contains__((row,col)):
                        cell_options.remove((row,col))

        print("number of flagged mines: " + str(num_flagged_mines))
        print("number of total mines: " + str(self.total_mines))

        # while visited_mines != total_mines
            # randomly select a cell
            # remove that cell from options list
            # open cell

                # if cell is safe
                    # gather info
                    # if clue - mn == hn
                        # flag every hidden neighbor as mine
                        # and set those neighbors to open/unsafe
                        # inc flagged_mines and visited mines
                    # if (8 - clue) - sn == hn
                        # mark every hidden neighbor as safe
                        # and set those neighbors to open
                # else: if cell is mine
                    # inc visited mines
                    # set is_safe to 0

    def gather_info(self, row, col):
        cell = self.env[row][col]
        for n in self.get_neighbors(row, col):
            if n[0].is_safe == 1:
                cell.safe_neighbors += 1
            elif n[0].is_safe == 0:
                cell.mine_neighbors += 1
            else:
                cell.hidden_neighbors += 1
        self.env[row][col] = cell



    def get_neighbors(self, row, col):
        neighbors = []
        dim = len(self.env)
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if self.valid(i, j, dim) and (i != row or j != col):
                    neighbors.append((self.env[i][j], (i, j)))
        return neighbors



    def valid(self, row, col, dim):
        if row >= 0 and col >= 0 and row < dim and col < dim:
            return True
        else:
            return False











