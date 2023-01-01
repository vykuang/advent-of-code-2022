#! /usr/bin/env python
"""
AoC 2022 Day
"""
import time
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
    def __repr__(self):
        return str(self.coords)

def path_find(root_pos: complex, grid: dict) -> PathNode:
    """
    Given root node, the grid, and the height dict,
    find the shortest way to "E"
    """
    
    root = PathNode(get_height(grid.get(root_pos)), root_pos)
    visited = {root_pos}
    unvisited = deque([root])
    logger.debug(f"root.coords: {root.coords}\theight: {root.height}")
    while unvisited:
        current = unvisited.popleft() # FIFO queue
        logger.debug(f"current.coords: {current.coords}\tht: {current.height}")
        if grid.get(current.coords) == "E":
            return current
        # children = find_children(current.coords)
        candidate_coords = [current.coords + way for way in [-1, 1, +1j, -1j]]
        logger.debug(f"candidates: {candidate_coords}")
#         children_info = [(ht, coord) for coord in candidate_coords if (ht := hmap[grid[coord.real][coord.imag]]) - current.height <= 1]
        children_info = [(ht, coord) for coord in candidate_coords
            if ((ht := get_height(grid.get(coord, '{'))) - current.height <= 1)]
        children = [PathNode(ht, coord, current) for (ht, coord) in children_info] 
        for child in children:
            if child.coords not in visited:
                unvisited.append(child)
        visited.add(current.coords)

def get_height(ch: str) -> int:
    """
    Use `ord()` to return int rep of string char
    Replaces 'S' with 'a' and 'E' with 'z'
    """
    ch = ch.replace('S', 'a').replace('E', 'z')
    return ord(ch) - ord('a')
    
def get_coord(idx: int, width: int) -> complex:
    """
    After reading a 2D array in as 1D vector, convert the 1D index to
    2D coordinate in the form of complex number by dividing by the
    original 2D row length:
        dividend = row
        remainder = col
    Thus if width = 5, list idx of 6 (7th element) would yield 1 r1, 
    and would return 1+1j to indicate (1, 1): row 1, col 1
    """
    div, remain = divmod(idx, width)
    return complex(div, remain)

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

    # read entire grid as one line
    grid = open(fp).read().replace('\n','')
    width = len(next(load_input(fp)))
    logger.debug(f"width: {width}")
    # build dict to use grid.get(complex_coord) and bypass the need for
    # integer list indices
    grid = {get_coord(x, width): grid[x] for x in range(len(grid))}
    logger.debug(f"{[item for item in grid][:5]}")
    top = path_find(0j, grid)
    logger.debug(f"E coord: {top.coords}")
    parent_coord = top.coords
    dist = 0
    while top.coords != complex():
        logger.debug(f"reversing coords:\t{top.coords}")
        top = top.parent
        dist += 1
    print(f"shortest distance: {dist}")
