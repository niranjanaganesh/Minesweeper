#creating a 2d grid in Python
"""import numpy as np
import matplotlib.pyplot as plt

plt.imshow(np.random.random((10,10)));
plt.colorbar()
plt.show()"""
import numpy as np
import pygame

class Cell:
    def __init__(self, value, mine_value, state):
        self.value = value # number of mines adj to this cell
        self.mine_value = mine_value # 0 if not mine, 1 if mine
        self.state = state # open or closed

    def __str__(self):
        cell_str = '{value: ' + str(self.value) + ', mine value: ' + str(self.mine_value) +\
                   ', state: ' + str(self.state) + '}'
        return cell_str

def print_grid(grid):
    dim = len(grid)
    for row in range(dim):
        for col in range(dim):
            print(str(grid[row][col]))


def update_values_backend(grid):
    # go to each mine
    # circle the mine
        # for each cell around the mine, if its not a mine itself
            # inc the value

    dim = len(grid)
    for row in range(dim): # Iterate through rows and cols
        for col in range(dim):
            if grid[row][col].mine_value == 1: # If mine found, it is central cell
                print('row: ' + str(row) + ' col: ' + str(col))
                for i in range(row-1, row+2):
                    for j in range(col-1, col+2):
                        if valid(i, j, dim) and (i != row or j != col): # If ij valid and not central cell
                            if grid[i][j].mine_value != 1: # If not mine in surrounding circle
                                grid[i][j].value += 1 # Inc that cell's value
                                print('i: ' + str(i) + ' j: ' + str(j) + ' value: ' + str(grid[i][j].value))

    return grid


def valid(row, col, dim):
    if row >= 0 and col >= 0 and row < dim and col < dim:
        return True
    else:
        return False


def update_values_frontend(grid, screen):
    zero = pygame.image.load('./images/0.png')
    one = pygame.image.load('./images/1.png')
    two = pygame.image.load('./images/2.png')
    three = pygame.image.load('./images/3.png')
    four = pygame.image.load('./images/4.png')
    five = pygame.image.load('./images/5.png')
    six = pygame.image.load('./images/6.png')
    seven = pygame.image.load('./images/7.png')
    eight = pygame.image.load('./images/8.png')

    dim = len(grid)
    x = 0
    y = 0
    for row in range(dim):
        if row > 0:
            y += 40
        for col in range(dim):
            x += 40
            print('x: ' + str(x) + ' y: ' + str(y))
            if grid[row][col].value == 0:
                pygame.Surface.blit(zero, screen, (x, y))
            """if grid[row][col].value == 1:
            if grid[row][col].value == 2:
            if grid[row][col].value == 3:
            if grid[row][col].value == 4:
            if grid[row][col].value == 5:
            if grid[row][col].value == 6:
            if grid[row][col].value == 7:
            if grid[row][col].value == 8:"""


def image_display(screen, filename, xy):
    img = pygame.image.load(filename)
    img = pygame.transform.scale(img, (40, 40))
    screen.blit(img, xy)


def main():

    # SETUP GRID
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BACKGROUND = (79, 159, 159)
    RED = (255, 0, 0)

    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 40
    HEIGHT = 40

    # This sets the margin between each cell
    MARGIN = 5

    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    grid = []
    # Get dimension input
    #dim = int(input('Enter dimension: '))
    dim = 10

    for row in range(dim):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(dim):
            cell = Cell(0, np.random.binomial(1, 0.125, 1), False)
            grid[row].append(cell)  # Append a cell

    grid = update_values_backend(grid)
    #print_grid(grid)

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = ((MARGIN + WIDTH) * dim + MARGIN, (MARGIN + WIDTH) * dim + MARGIN)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Minesweeper")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
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
        """zero = pygame.image.load('./images/0.png')
        one = pygame.image.load('./images/1.png')
        two = pygame.image.load('./images/2.png')
        three = pygame.image.load('./images/3.png')
        four = pygame.image.load('./images/4.png')
        five = pygame.image.load('./images/5.png')
        six = pygame.image.load('./images/6.png')p
        seven = pygame.image.load('./images/7.png')
        eight = pygame.image.load('./images/8.png')"""

        x = 5
        y = 5
        # Draw the grid
        for row in range(10):
            if row > 0:
                y += 45
            for col in range(10):
                color = WHITE
                if grid[row][col].mine_value == 1:
                    color = BLACK
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * col + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

                if grid[row][col].value == 0:
                    image_display(screen, './images/0.png', (x,y))
                if grid[row][col].value == 1:
                    image_display(screen, './images/1.png', (x, y))
                if grid[row][col].value == 2:
                    image_display(screen, './images/2.png', (x, y))
                if grid[row][col].value == 3:
                    image_display(screen, './images/3.png', (x, y))
                if grid[row][col].value == 4:
                    image_display(screen, './images/4.png', (x, y))
                if grid[row][col].value == 5:
                    image_display(screen, './images/5.png', (x, y))
                if grid[row][col].value == 6:
                    image_display(screen, './images/6.png', (x, y))
                if grid[row][col].value == 7:
                    image_display(screen, './images/7.png', (x, y))
                if grid[row][col].value == 8:
                    image_display(screen, './images/8.png', (x, y))

                x += 45


        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()


if __name__ == '__main__':
    main()