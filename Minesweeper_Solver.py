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
        self.group_pairs_cache = None

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
    def group_pairs(self):
        if self.group_pairs_cache is None:
            group_pairs = set()
            previous = set()
            for closed_coord in self.closed_coords:
                if closed_coord not in previous:
                    if any(adj_coord in self.indicator_coords for adj_coord in self.adjacency_cache[closed_coord]):
                        indicator_group = set()
                        closed_group = set()
                        new_closed_coords = {closed_coord}

                        while new_closed_coords:
                            closed_coords = new_closed_coords
                            new_closed_coords = set()

                            for closed_coord in closed_coords:
                                for adj_coord in self.adjacency_cache[closed_coord]:
                                    if adj_coord in self.indicator_coords:
                                        if adj_coord not in previous:
                                            previous.add(adj_coord)
                                            indicator_group.add(adj_coord)

                                        for doubly_adj_coord in self.adjacency_cache[adj_coord]:
                                            if doubly_adj_coord not in previous and doubly_adj_coord in self.closed_coords:
                                                previous.add(doubly_adj_coord)
                                                closed_group.add(doubly_adj_coord)
                                                new_closed_coords.add(doubly_adj_coord)

                        group_pairs.add((frozenset(indicator_group), frozenset(closed_group)))

            self.group_pairs_cache = group_pairs
        return self.group_pairs_cache

    def mine_probabilities(self):
        #{closed_groups: {(flag_counts, arrangement_counts): {coords: flag_occurances})}}
        def arrangement_data(closed_coords, indicator_coords, ):
        
        def combined(prob_data):
            prob_data = list(prob_data.items())
            combined_prob_data = prob_data.pop(0)

            def combine(a, b):
                combined_prob_data = {}
                a_closed_group, a_arrangement_data = a
                b_closed_group, b_arrangement_data = b
                closed_group = a_closed_group | b_closed_group
                combined_prob_data[closed_group] = {}
                for (a_flag_count, a_arrangement_count), a_coord_data in a_arrangement_data.items():
                    for (b_flag_count, b_arrangement_count), b_coord_data in b_arrangement_data.items():
                        flag_count = a_flag_count + b_flag_count
                        arrangement_count = a_arrangement_count * b_arrangement_count
                        combined_prob_data[closed_group][(flag_count, arrangement_count)] = {}
                        for coord, flag_occurances in a_coord_data.items():
                            combined_prob_data[closed_group][(flag_count, arrangement_count)][coord] = flag_occurances*b_arrangement_count
                        for coord, flag_occurances in b_coord_data.items():
                            combined_prob_data[closed_group][(flag_count, arrangement_count)][coord] = flag_occurances*a_arrangement_count
                return combined_prob_data

            for data in self.closed_coords:
                combined_prob_data = combine(combined_prob_data, data)

            return combined_prob_data


        mine_probabilities = np.zeros_like(self.grid)

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

visualiser = np.zeros_like(test.grid)
for indicator_group, closed_group in test.group_pairs:
    for coord in indicator_group:
        visualiser[coord] = -1
    for coord in closed_group:
        visualiser[coord] = 1
print(visualiser)