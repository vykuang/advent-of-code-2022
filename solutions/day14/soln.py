#! /usr/bin/env python
"""
AoC 2022 Day 14 - Falling sands
"""
import sys
import logging

import numpy as np

logger = logging.getLogger(__name__)

def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

def delta_sign(a, b):
    """
    Returns 1 if b > a, and -1 if b < a
    """
    return int((b - a)/abs(b - a))

def make_rock(rock_line: list) -> np.array:
    """
    Converts list of vertices into coordinates of edges

    Returns a bool array
    """
    logger.debug(f"new rock_line:")
    edges = [tuple(rock_line[-1])]
    for i in range(len(rock_line) - 1):
        x, y = rock_line[i]
        nx, ny = rock_line[i + 1]
        if x != nx:
            fill = [(dx, y) for dx in range(x, nx, delta_sign(x, nx))]
#             x_fill = np.array(range(x, nx, delta_sign(x, nx)))
#             y_fill = np.full(len(x_fill), y)
#         else:
#             y_fill = np.array(range(y, ny, delta_sign(y, ny)))
#             x_fill = np.full(len(y_fill), x)
        else:
            fill = [(x, dy) for dy in range(y, ny, delta_sign(y, ny))]
        logger.debug(f"rock segment: ")
        logger.debug(fill)
        edges.extend(fill)
    return edges

if __name__ == "__main__":
    fn = sys.argv[1]
    match fn:
        case "test" | "input":
            fp = f"{fn}.txt"
            test = fn == "test" 
        case _:
            raise ValueError(f"{fn} cannot be used")
            
    if test:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
    else:
        logger.setLevel(logging.INFO)
    convert_xy = lambda xy_str: list(int(xy) for xy in xy_str.split(','))
    rocks = [[convert_xy(xy) for xy in line.split() if ',' in xy] for line in load_input(fp)]
    cave = [make_rock(edge) for edge in rocks]
    logger.debug(f"cave:\n{cave}")
