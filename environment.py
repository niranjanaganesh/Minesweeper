#creating a 2d grid in Python
"""import numpy as np
import matplotlib.pyplot as plt

plt.imshow(np.random.random((10,10)));
plt.colorbar()
plt.show()"""
import numpy as np
import pygame

from agent import Agent
from csp_agent import CSPAgent

class Cell:
    def __init__(self, value, mine_value, is_open, id):
        self.value = value  # number of mines adj to this cell
        self.mine_value = mine_value  # 0 if not mine, 1 if mine
        self.is_open = is_open  # true if open, false if closed
        self.id = id

        # properties that the agent updates on its board
        self.is_safe = -1  # 0 if not, 1 if safe, -1 if hidden
        self.safe_neighbors = 0  # num safe squares identified around it
        self.mine_neighbors = 0  # num mines identified around it
        self.hidden_neighbors = 0 # num hidden neighbors around it
        self.is_flagged = False

    def __str__(self):
        cell_str = '{value: ' + str(self.value) + ', mine value: ' + str(self.mine_value) +\
                   ', state: ' + str(self.is_open) + '}'
        cell_props = '{is safe: ' + str(self.is_safe) + ', #sn: ' \
                     + str(self.safe_neighbors) + ', #mn: ' \
                     + str(self.mine_neighbors) + ', #hn: ' + str(self.hidden_neighbors) + '}'
        return '\n' + cell_str + '\n' + cell_props

def print_grid(grid):
    dim = len(grid)
    for row in range(dim):
        for col in range(dim):
            if not grid[row][col].is_open:
                print('X', end='  ')
            else:
                extra_char = ''
                space = '  '
                if grid[row][col].is_safe == 1:
                    extra_char = '*'
                    space = ' '
                if grid[row][col].mine_value == 0:
                    print(str(grid[row][col].value) + str(extra_char), end=space)
                if grid[row][col].mine_value == 1:
                    if grid[row][col].is_flagged:
                        print('F', end=space)
                    else:
                        print('M', end=space)
        print('')


"""Updates the clue for each cell"""
def update_clues(grid):
    # go to each mine
    # circle the mine
        # for each cell around the mine, if its not a mine itself
            # inc the value

    dim = len(grid)
    for row in range(dim): # Iterate through rows and cols
        for col in range(dim):
            if grid[row][col].mine_value == 1: # If mine found, it is central cell
                #print('row: ' + str(row) + ' col: ' + str(col))
                for i in range(row-1, row+2):
                    for j in range(col-1, col+2):
                        if valid(i, j, dim) and (i != row or j != col): # If ij valid and not central cell
                            if grid[i][j].mine_value != 1: # If not mine in surrounding circle
                                grid[i][j].value += 1 # Inc that cell's value
                                #print('i: ' + str(i) + ' j: ' + str(j) + ' value: ' + str(grid[i][j].value))

    return grid


def valid(row, col, dim):
    if row >= 0 and col >= 0 and row < dim and col < dim:
        return True
    else:
        return False

def display_image(screen, filename, xy):
    img = pygame.image.load(filename)
    img = pygame.transform.scale(img, (40, 40))
    screen.blit(img, xy)

def open_cell(grid, row, col):
    grid[row][col].is_open = True

def main():

    """""""""""""""""""""""""""""""GRID SETUP"""""""""""""""""""""""""""""""

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BACKGROUND = (79, 159, 159)
    MAROON = (128, 0, 0)
    GREEN = (0, 128, 0)
    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 40
    HEIGHT = 40
    # This sets the margin between each cell
    MARGIN = 5
    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    grid = []

    # Get dimension input
    # dim = int(input('Enter dimension: '))
    dim = 3
    total_mines = 0

    for row in range(dim):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(dim):
            cid = str(row) + '.' + str(column)
            if row == 0 and column == 0:
                cell = Cell(0, 0, False, cid)
                grid[row].append(cell)
            else:
                num = np.random.binomial(1, 0.2, 1)
                cell = Cell(0, num, False, cid)
                if num == 1:
                    total_mines += 1
                grid[row].append(cell)  # Append a cell

    grid = update_clues(grid)
    print_grid(grid)

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = ((MARGIN + WIDTH) * dim + MARGIN, (MARGIN + WIDTH) * dim + MARGIN)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Minesweeper")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    """""""""""""""""""""""""""""""MAIN PROGRAM LOOP"""""""""""""""""""""""""""""""
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # --- Game logic should go here


        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BACKGROUND)


        # --- Drawing code should go here

        x = 5
        y = 5
        # Draw the grid
        for row in range(dim):
            for col in range(dim):
                color = WHITE
                if grid[row][col].mine_value == 1:
                    color = BLACK
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * col + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

                if grid[row][col].mine_value != 1:# not a mine
                    if grid[row][col].value == 0:
                        display_image(screen, './images/0.png', (x,y))
                    if grid[row][col].value == 1:
                        display_image(screen, './images/1.png', (x, y))
                    if grid[row][col].value == 2:
                        display_image(screen, './images/2.png', (x, y))
                    if grid[row][col].value == 3:
                        display_image(screen, './images/3.png', (x, y))
                    if grid[row][col].value == 4:
                        display_image(screen, './images/4.png', (x, y))
                    if grid[row][col].value == 5:
                        display_image(screen, './images/5.png', (x, y))
                    if grid[row][col].value == 6:
                        display_image(screen, './images/6.png', (x, y))
                    if grid[row][col].value == 7:
                        display_image(screen, './images/7.png', (x, y))
                    if grid[row][col].value == 8:
                        display_image(screen, './images/8.png', (x, y))
                x += 45

                # This will only display a maroon cell for covered cells
                if not grid[row][col].is_open:
                    color = MAROON
                    pygame.draw.rect(screen,
                                     color,
                                     [(MARGIN + WIDTH) * col + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT])

                if grid[row][col].is_flagged:
                    color = GREEN
                    pygame.draw.rect(screen,
                                     color,
                                     [(MARGIN + WIDTH) * col + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT])
            x = 5
            y += 45

        #grid[0][0].is_open = True

        # Interact with the agent here
        #agent = Agent(grid, total_mines)
        #grid = agent.start()
        #grid = agent.naive_solver()

        agent = CSPAgent(grid, total_mines)
        agent.csp_solver()
        done = True


        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()


if __name__ == '__main__':
    main()