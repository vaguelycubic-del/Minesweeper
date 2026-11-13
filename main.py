import numpy as np
# closed: 9
# flag: 10
#


class Minesweeper:
    class Loss(Exception): pass

    def __init__(self, shape=(0, 0)):
        self.shape = shape
        self.grid = np.zeros(shape, dtype=int)
        self.closed = np.full(shape, True, dtype=bool)
        self.flags = np.full(shape, False, dtype=bool)

        self.coords = frozenset((y, x) for y in range(self.shape[0]) for x in range(self.shape[1]))

        self.adjacency_cache = {}
        for coord in self.coords:
            y, x = coord
            for adj_y in range(y-1, y+2):
                for adj_x in range(x-1, x+2):
                    adj_coord = (adj_y, adj_x)
                    if adj_coord in self.coords:
                        self.adjacency_cache[coord].add(adj_coord)
        for coord, adj_coords in self.adjacency_cache.items():
            self.adjacency_cache[coord] = frozenset(adj_coords)


        self.view_cache = None




    # PROPERTIES
    @property
    def view(self):
        if self.view_cache is None:
            view_cache = self.grid.copy()
            for coord, closed in np.ndenumerate(self.closed):
                if closed:
                    view_cache[coord] = 9

            for coord, flag in np.ndenumerate(self.flags):
                if flag:
                    view_cache[coord] = 9
            self.view_cache = view_cache


        return self.view_cache



    # ACTIONS
    def flag(self, coord):
        if self.closed[coord]:
            self.closed[coord] = False
            self.flags[coord] = True

    def open(self, coord):
        if self.closed[coord]:
            if self.grid[coord] == -1:
                raise self.Loss()

            self.closed[coord] = False

            previous = set(coord)
            adj_coords = {coord}

            while adj_coords:
                coords = adj_coords
                adj_coords = set()

                for coord in coords:
                    for adj_coord in self.adjacency_cache[coord]:
                        if adj_coord not in previous:
                            if self.grid[adj_coord] == 0 or (self.grid[adj_coord] in range(1, 9) and self.grid[coord] == 0):
                                self.closed[adj_coord] = False
                                previous.add(adj_coord)
                                adj_coords.add(adj_coord)

        self.clear_caches()


    def clear_caches(self):
        self.view_cache = None


    def clear_adj_group(self, start_coord):



