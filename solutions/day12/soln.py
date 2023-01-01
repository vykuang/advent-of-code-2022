#! /usr/bin/env python
"""
AoC 2022 Day
"""

import sys
import logging
from string import ascii_lowercase
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

class PathNode:
    def __init__(self, height: int, coords: complex, parent=None):
        self.height = height
        self.coords = coords
        self.parent = parent

def map_grid(grid_line: str, height_map: dict):
    """Maps the grid from letters to int height via height_map
    """
    return [height_map[h] for h in grid_line]


def path_find(root_pos: complex, grid: list, hmap: dict) -> PathNode:
    """
    Given root node, the grid, and the height dict,
    find the shortest way to "E"
    """
    root = PathNode(grid[root_pos.real][root_pos.imag])
    unvisited = deque([root])

    while unvisited:
        current = unvisited.popleft() # FIFO queue
        if grid[current.real][current.imag] == "E":
            return current
        # children = find_children(current.coords)
        candidate_coords = [current.coords + way for way in [-1, 1, +1j, -1j]]
        children_info = [(ht, coord) for coord in candidate_coords if (ht := hmap[grid[coord.real][coord.imag]]) - current.height <= 1]
        children = [PathNode(h, coord, current) for (h, coord) in children_info]
        for child in children:
            child.parent = current
            unvisited.append(child)
     
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
    hmap = dict(zip(ascii_lowercase, range(len(ascii_lowercase))))
    hmap.update({"S": 0, "E":26})

    grid = [line for line in load_input(fp)]
    # pmapped_grid = [map_grid(line) for line in grid]
    top = path_find(complex(0), grid, hmap)
    logger.debug(f"Node found: {grid[top.real][top.imag]}, ht: {top.height}, coord: {top.coords}")

