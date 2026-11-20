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

    @property
    def mine_probabilities(self):
        #{closed_groups: {flag_counts: arrangement_counts}
        #{closed_groups: {flag_counts: {coords: flag_occurances}}}

        arrangements_data = {}
        coord_data = {}
        for indicator_coords, closed_coords in self.group_pairs:
            def backtrack(unseen_coords, seen_coords, grid=self.grid, flag_count=len(self.flag_coords)):
                if len(unseen_coords) == 0:
                    coord_data.setdefault(closed_coords, {}).setdefault(flag_count, {})
                    arrangements_data.setdefault(closed_coords, {}).setdefault(flag_count, 0)
                    arrangements_data[closed_coords][flag_count] += 1
                    for coord in seen_coords | self.flag_coords:
                        coord_data[closed_coords][flag_count].setdefault(coord, 0)
                        if grid[coord] == 10:
                            coord_data[closed_coords][flag_count][coord] += 1
                    return
                else:
                    coord = unseen_coords.pop()
                    seen_coords.add(coord)
                    value = grid[coord]
                    def flag_invalidates():
                        for adj_coord in self.adjacent_coords(coord):
                            if adj_coord in self.indicator_coords:
                                _value = grid[adj_coord]
                                doubly_adj_flags = len(tuple(doubly_adj_coord for doubly_adj_coord in self.adjacent_coords(adj_coord) if grid[doubly_adj_coord] == 10))
                                if doubly_adj_flags > _value:
                                    return True
                        return False

                    def open_invalidates():
                        for adj_coord in self.adjacent_coords(coord):
                            if adj_coord in self.indicator_coords:
                                _value = grid[adj_coord]
                                doubly_adj_coords = self.adjacent_coords(adj_coord)
                                doubly_adj_unseen = len(unseen_coords & doubly_adj_coords)
                                doubly_adj_flags = len(tuple(doubly_adj_coord for doubly_adj_coord in doubly_adj_coords if grid[doubly_adj_coord] == 10))
                                if (_value - doubly_adj_flags) > doubly_adj_unseen:
                                    return True

                        return False

                    for flag in (True, False):
                        if flag:
                            grid[coord] = 10
                            if not flag_invalidates() and flag_count < self.mine_count:
                                backtrack(unseen_coords, seen_coords, grid, flag_count + 1)

                            grid[coord] = value
                        else:
                            if not open_invalidates():
                                backtrack(unseen_coords, seen_coords, grid, flag_count)

                    seen_coords.remove(coord)
                    unseen_coords.add(coord)

            backtrack(set(closed_coords), set())

        global_closed_coords = set()
        combined_coord_data = {0:{}}
        combined_arrangements_data = {0:1}
        for closed_coords, flag_counts in coord_data.items():
            global_closed_coords.update(closed_coords)
            new_combined_coord_data = {}
            new_combined_arrangements_data = {}
            
            for c_flag_count, c_coords in combined_coord_data.items():
                for flag_count, coords in flag_counts.items():
                    new_flag_count = c_flag_count+flag_count
                    new_combined_coord_data.setdefault(new_flag_count, {})
                    
                    c_arrangements_count = combined_arrangements_data[c_flag_count]
                    arrangements_count = arrangements_data[closed_coords][flag_count]
                    
                    for c_coord, c_flag_occurances in c_coords.items():
                        new_combined_coord_data[new_flag_count].setdefault(c_coord, 0)
                        new_combined_coord_data[new_flag_count][c_coord] += arrangements_count*c_flag_occurances
                    
                    for coord, flag_occurances in coords.items():
                        new_combined_coord_data[new_flag_count].setdefault(coord, 0)
                        new_combined_coord_data[new_flag_count][coord] += c_arrangements_count*flag_occurances
                    
                    new_combined_arrangements_data.setdefault(new_flag_count, 0)
                    new_combined_arrangements_data[new_flag_count] += c_arrangements_count * arrangements_count
            
            combined_coord_data = new_combined_coord_data
            combined_arrangements_data = new_combined_arrangements_data

        mine_probabilities = np.zeros_like(self.grid, dtype=float)

        independent_closed_coords = self.closed_coords - global_closed_coords
        global_arrangements_count = 0
        for flag_count, coords in combined_coord_data.items():
            independent_mine_count = self.mine_count-flag_count
            closed_arrangements_count = math.comb(len(independent_closed_coords), independent_mine_count)
            global_arrangements_count += closed_arrangements_count * combined_arrangements_data[flag_count]
            for coord, flag_occurances in coords.items():
                mine_probabilities[coord] += flag_occurances * closed_arrangements_count
            for coord in independent_closed_coords:
                mine_probabilities[coord] += independent_mine_count/len(independent_closed_coords)
            
        mine_probabilities /= global_arrangements_count
        return mine_probabilities
        
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


test = Minesweeper_Solver(grid, 50)

print(tuple(test.group_pairs)[0][1])
print(test.mine_probabilities)

