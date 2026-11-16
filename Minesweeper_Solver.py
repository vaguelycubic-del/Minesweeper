import numpy as np
import math

class Minesweeper_Solver:
    # SETUP
    def __init__(self, grid, mine_count):
        self.grid = grid
        self.mine_count = mine_count
        self.shape = grid.shape

        self.coords = frozenset((y, x) for y in range(self.shape[0]) for x in range(self.shape[1]))

        self.adjacency_cache = {}
        for coord in self.coords:
            y, x = coord
            for adj_y in range(y - 1, y + 2):
                for adj_x in range(x - 1, x + 2):
                    adj_coord = (adj_y, adj_x)
                    if adj_coord in self.coords:
                        self.adjacency_cache.setdefault(coord, set()).add(adj_coord)
        for coord, adj_coords in self.adjacency_cache.items():
            self.adjacency_cache[coord] = frozenset(adj_coords)

        self.indicator_coords_cache = None
        self.closed_coords_cache = None
        self.flag_coords_cache = None
        self.relevant_indicator_coords_cache = None
        self.relevant_closed_coords_cache = None
        self.relevant_indicator_coord_groups_cache = None
        self.relevant_closed_coord_groups_cache = None

        self.mine_probability_cache = None

    # PROPERTIES
    @property
    def flag_coords(self):
        if self.flag_coords_cache is None:
            self.flag_coords_cache = frozenset(coord for coord, value in np.ndenumerate(self.grid) if value == 10)
        return self.flag_coords_cache

    @property
    def indicator_coords(self):
        if self.indicator_coords_cache is None:
            self.indicator_coords_cache = frozenset(coord for coord, value in np.ndenumerate(self.grid) if value in range(1, 9))
        return self.indicator_coords_cache

    @property
    def closed_coords(self):
        if self.closed_coords_cache is None:
            self.closed_coords_cache = frozenset(coord for coord, value in np.ndenumerate(self.grid) if value == 9)
        return self.closed_coords_cache

    @property
    def relevant_indicator_coords(self):
        if self.relevant_indicator_coords_cache is None:
            relevant_indicator_coords_cache = set()
            for coord in self.indicator_coords:
                if any(adj_coord in self.closed_coords for adj_coord in self.adjacent_coords(coord)):
                    relevant_indicator_coords_cache.add(coord)
            self.relevant_indicator_coords_cache = frozenset(relevant_indicator_coords_cache)
        return self.relevant_indicator_coords_cache

    @property
    def relevant_closed_coords(self):
        if self.relevant_closed_coords_cache is None:
            relevant_closed_coords_cache = set()
            for coord in self.closed_coords:
                if any(adj_coord in self.indicator_coords for adj_coord in self.adjacent_coords(coord)):
                    relevant_closed_coords_cache.add(coord)
            self.relevant_closed_coords_cache = frozenset(relevant_closed_coords_cache)
        return self.relevant_closed_coords_cache

    @property
    def relevant_indicator_coord_groups(self):
        if self.relevant_indicator_coord_groups_cache is None:
            relevant_indicator_coord_groups_cache = set()

            previous = set()
            for coord in self.indicator_coords:
                if coord not in previous:
                    group = {coord}
                    def shares_indicator_neighbour(a, b):
                        for adj_coord in self.adjacent_coords(a):
                            if self.grid[adj_coord] in range(1, 9):
                                if adj_coord in self.adjacent_coords(b):
                                    return True

                        return False

                    for adj_coord in self.adjacent_coords(coord):
                        if shares_indicator_neighbour(coord, adj_coord):
                            group.add(adj_coord)




    @property
    def mine_probabilities(self):
        if self.mine_probability_cache is None:
            def flag_oversaturates_indicators(coord, grid):
                for adj_coord in self.adjacent_coords(coord):
                    value = grid[adj_coord]
                    if value != 9:
                        if sum(grid[adj_adj_coord] == 10 for adj_adj_coord in self.adjacent_coords(adj_coord)) > value:
                            return True
                return False


            def combine(a, b):
                combined = {}
                for a_closed_coord_group, a_data in a.items():
                    for b_closed_coord_group, b_flag_count_data in b.items():
                        combined[a_closed_coord_group+b_closed_coord_group] = a_flag_count + b_flag_count
                        for



        return self.mine_probability_cache

    # UTILITIES
    def adjacent_coords(self, coord):
        return self.adjacency_cache.get(coord, frozenset())

grid = np.array([
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
    [9, 2, 1, 2, 9, 9, 9, 9, 9, 9],
    [9, 1, 0, 1, 2, 9, 9, 9, 9, 9],
    [9, 1, 0, 0, 1, 1, 1, 9, 9, 9],
    [9, 1, 1, 0, 0, 0, 1, 9, 9, 9],
    [9, 9, 1, 0, 0, 1, 2, 9, 9, 9],
    [9, 9, 2, 1, 1, 1, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
])

test = Minesweeper_Solver(grid, 15)

print(test.mine_probabilities)