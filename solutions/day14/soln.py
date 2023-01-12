#! /usr/bin/env python
"""
AoC 2022 Day 14 - Falling sands
"""
import sys
import logging
from itertools import chain
import numpy as np
from scipy.sparse import coo_matrix, dok_matrix

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()


def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line


def delta_sign(a, b):
    """
    Returns 1 if b > a, and -1 if b < a
    """
    return int((b - a) / abs(b - a))


def make_rock_xy(rock_line: list) -> list:
    """
    Converts list of vertices into coordinates of edges

    Returns a list of tuple coordinates
    """
    logger.debug("new rock_line:")
    edges = [tuple(rock_line[-1])]
    for i in range(len(rock_line) - 1):
        x, y = rock_line[i]
        nx, ny = rock_line[i + 1]
        if x != nx:
            fill = [(dx, y) for dx in range(x, nx, delta_sign(x, nx))]
        else:
            fill = [(x, dy) for dy in range(y, ny, delta_sign(y, ny))]
        logger.debug(f"rock segment: \n{fill}")
        edges.extend(fill)

    return edges


def find_sand_rest(origin: tuple(int, int), cave: dok_matrix) -> tuple(int, int) | None:
    """
    Given origin sand coordinates and the existing cave map,
    determine the coordinate of the resting position

    Returns
    -------
    xy: tuple(int, int) | None
        resting coordinate, if exists; None if it does not.
    """


if __name__ == "__main__":
    fn = sys.argv[1]
    match fn:
        case "test" | "input":
            fp = f"{fn}.txt"
            test = fn == "test"
        case _:
            raise ValueError(f"{fn} cannot be used")

    if test:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    logger.setLevel(loglevel)
    ch.setLevel(loglevel)
    logger.addHandler(ch)

    # converts from "x,y" to [x, y]
    convert_xy = lambda xy_str: list(int(xy) for xy in xy_str.split(","))
    rocks = [
        [convert_xy(xy) for xy in line.split() if "," in xy] for line in load_input(fp)
    ]
    cave = [make_rock_xy(edge) for edge in rocks]
    logger.debug(f"cave:\n{cave}")

    cave = list(chain(*cave))
    logger.debug(f"chained cave:\n{cave}")

    ys, xs = list(zip(*cave))
    logger.debug(f"xs:\n{xs}\nys:\n{ys}")

    # can also consider dict-of-keys array for construction
    # coo does not allow indexing, but dok does
    # however coo construction is considered fast
    cave_sparse = coo_matrix((np.ones(len(xs)), (xs, ys)), dtype=bool)
    logger.debug(f"cave map: \n{cave_sparse.toarray()[:,min(ys):]}")

    cave_sparse = cave_sparse.todok()
    # inverse of problem spec to match (x, y) convention to (row, col)
    ORIGIN = (0, 500)
    sand_xy = ORIGIN
    sand_count = 0
    while sand_xy := find_sand_rest(ORIGIN, cave_sparse):
        cave_sparse[sand_xy] = True
        sand_count += 1

    print(f"sands to abyss: {sand_count}")
