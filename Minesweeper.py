import numpy as np
import random
# closed: 9
# flag: 10
# mine: -1


class Minesweeper:
    class Failure(Exception): pass
    class Success(Exception): pass
        
    # SETUP
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
                        self.adjacency_cache.setdefault(coord, set()).add(adj_coord)

        for coord, adj_coords in self.adjacency_cache.items():
            self.adjacency_cache[coord] = frozenset(adj_coords)


        self.view_cache = None

    def scatter_mines(self, mine_count=0):
        coords = set(self.coords)
        for _ in range(mine_count):
            coord = random.choice(tuple(coords))
            coords.remove(coord)
            self.grid[coord] = -1
            for adj_coord in self.adjacent_coords(coord):
                value = self.grid[adj_coord]
                if value != -1:
                    self.grid[adj_coord] = value+1

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
                raise self.Failure()

            self.closed[coord] = False

            previous = {coord,}
            adj_coords = {coord,}

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

        self.view_cache = None

    # DUNDERS
    def __str__(self):
        return str(self.view)

    # UTILITIES
    def adjacent_coords(self, coord):
        return self.adjacency_cache.get(coord, frozenset())

test = Minesweeper(shape=(10, 10))
test.scatter_mines(mine_count=50)
test.open(random.choice(tuple(test.coords)))
print(test)
print()
print(test.grid)


