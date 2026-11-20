import numpy as np
import Minesweeper
from Minesweeper import Minesweeper as minesweeper
from Minesweeper_Solver import Minesweeper_Solver as solver

ms1 = minesweeper((10, 10))
ms1.scatter_mines(15)
try:
    ms1.open((5, 5))
except Minesweeper.FailureError:
    print('break failed')
print(ms1)

solver = solver(ms1.view, ms1.mine_count)
print(solver.mine_probabilities)

for coord, mine_probability in np.ndenumerate(solver.mine_probabilities):
    print(mine_probability)
    if mine_probability < 10**-2:
        ms1.open(coord)
    if mine_probability > 1-10**-2:
        ms1.flag(coord)

print(ms1)