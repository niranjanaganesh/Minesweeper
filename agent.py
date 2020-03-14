

class Agent:
    def __init__(self, env):
        self.env = env

    def start(self):
        # open first cell
        self.env = self.env.open_cell(self.env, 0, 0)

    def naive_solver(self):
        self.start()

        # get neighbors
        neighbors = self.get_neighbors(0, 0)


    def get_neighbors(self, row, col):
        neighbors = []
        dim = len(self.env)
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if self.valid(i, j, dim) and (i != row or j != col):
                    neighbors.append(self.env[i][j])
        return neighbors



    def valid(self, row, col, dim):
        if row >= 0 and col >= 0 and row < dim and col < dim:
            return True
        else:
            return False










