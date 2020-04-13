import numpy as np
import random


class Equation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class CSPAgent:
    def __init__(self, env, total_mines):
        self.env = env
        self.total_mines = total_mines
        self.visited_mines = 0
        self.flagged_mines = 0

    def csp_solver(self):
        # init vars
        dim = len(self.env)

        # init lists
        non_mines = []
        mines = []
        eqs = {}

        # generate list of cell position options
        cell_options = [(i, j) for i in np.arange(0, dim) for j in np.arange(0, dim)]

        # begin process
        while self.visited_mines < self.total_mines:

            # randomly select a cell
            if len(cell_options) == 0:  # if cell options is empty
                break
            pos = random.choice(cell_options)
            row = pos[0]
            col = pos[1]
            cell_options.remove(pos)  # remove from list of options
            cell = self.env[row][col]

            # open cell
            cell.is_open = True

            # if cell is not a mine
            if cell.mine_value == 0:
                cell.is_safe = 1  # mark cell as safe
                non_mines.append(cell.id)  # add to non_mines

                # generate equations for non-zero non-mines
                if cell.value != 0:
                    equation = self.get_equation(row, col)  # generate equation
                    eqs[cell.id] = equation  # add to eqs dict

                # if equations list is not empty
                if len(eqs) != 0:
                    for cid in eqs:
                        CSPAgent.update_non_mines(eqs[cid], non_mines)  # update eqs by removing non-mines
                        CSPAgent.update_mines(eqs[cid], mines)  # update eqs by removing mines and dec left side
                        if eqs[cid].left == 1 and len(eqs[cid].right) == 1:
                            mines.append(eqs[cid].right[0])  # found a new mine
                        if eqs[cid].left == 0 and len(eqs[cid].right) == 1:
                            non_mines.append(eqs[cid].right[0])  # found a new non-mine

                # gather info from nearby cells
                """self.gather_info(pos[0], pos[1])

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
                            n[0].is_open = True"""

            # if cell is mine (and you exploded a mine)
            elif cell.mine_value == 1:
                cell.is_safe = 0 # indicate that cell is unsafe
                mines.append(cell.id)
                self.visited_mines += 1
                #cell.is_safe = 0  # indicate cell is unsafe

            # print equations
            print('printing equations..')
            CSPAgent.print_eqs(eqs)

            # update grid
            self.update_grid(mines, non_mines)

            # clear mines
            mines.clear()

            #print(cell)
            print(row, col)
            self.print_env()
            print('-------')
            self.flagged_mines = self.total_mines

            # remove opened cells from options
            for row in range(dim):
                for col in range(dim):
                    if self.env[row][col].is_open and cell_options.__contains__((row, col)):
                        cell_options.remove((row, col))

        print("number of flagged mines: " + str(self.flagged_mines))
        print("number of total mines: " + str(self.total_mines))

    def update_grid(self, mines, non_mines):
        for mine in mines:
            row = int(mine.split('.')[0])
            col = int(mine.split('.')[1])
            if self.env[row][col].is_safe != 0:
                self.env[row][col].is_flagged = True
                self.flagged_mines += 1  # mines should only contain new flagged mines
                self.visited_mines += 1

        for non_mine in non_mines:
            row = int(non_mine.split('.')[0])
            col = int(non_mine.split('.')[1])
            self.env[row][col].is_safe = 1

    @staticmethod
    def update_non_mines(eq, non_mines):
        for elem in non_mines:
            if elem in eq.right:
                eq.right.remove(elem)

    @staticmethod
    def update_mines(eq, mines):
        for elem in mines:
            if elem in eq.right:
                eq.right.remove(elem)
                if eq.left > 0:
                    eq.left -= 1

    def get_equation(self, row, col):
        hidden_neighbors = []  # these are the actual hidden neighbors, not the count
        for n in self.get_neighbors(row, col):
            if not n[0].is_open:
                hidden_neighbors.append(n[0].id)

        return Equation(self.env[row][col].value, hidden_neighbors)

    def get_neighbors(self, row, col):
        neighbors = []
        dim = len(self.env)
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if self.valid(i, j, dim) and (i != row or j != col):
                    neighbors.append((self.env[i][j], (i, j)))
        return neighbors

    @staticmethod
    def print_eqs(eqs):
        for cid in eqs:
            print('cell id: ' + str(cid) + ', eqn: ' + str(eqs[cid].left) + ' = ' + CSPAgent.print_eq(eqs[cid]))

    @staticmethod
    def print_eq(eq):
        eq_str = ''
        for term in eq.right:
            eq_str += str(term) + ' '
        return eq_str

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
                            print('F', end='  ')
            print('')

    def valid(self, row, col, dim):
        if 0 <= row < dim and 0 <= col < dim:
            return True
        else:
            return False