import numpy as np
import Minesweeper
from Minesweeper import Minesweeper
from Minesweeper_Solver import Minesweeper_Solver as Solver

while True:
    ms1 = Minesweeper((10, 10))
    ms1.scatter_mines(15)
    try:
        ms1.open((5, 5))
    except Minesweeper.Failure:
        continue
    break

solver = Solver(ms1.view, ms1.mine_count)

while True:
    for coord in solver.open_targets:
        ms1.open(coord)

    for coord in solver.flag_targets:
        ms1.flag(coord)

    solver.update(ms1.view)
