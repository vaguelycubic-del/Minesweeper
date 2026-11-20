import numpy as np
import Minesweeper
from Minesweeper import Minesweeper as minesweeper
from Minesweeper_Solver import Minesweeper_Solver as solver

ms1 = minesweeper((10, 10))
ms1.scatter_mines(15)
try:
    ms1.open((5, 5))
except Minesweeper.Minesweeper.Failure:
    print('break failed')

solver = solver(ms1.view, ms1.mine_count)

for coord, mine_probability in np.ndenumerate(solver.mine_probabilities):
    if mine_probability == 0:
        ms1.open(coord)
    if mine_probability == 1:
        ms1.flag(coord)

print(ms1)
print(ms1.grid[5, 5])