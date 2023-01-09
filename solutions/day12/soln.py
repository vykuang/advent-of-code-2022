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


def path_find(root_pos: complex, grid: dict):
    """
    Given root node, the grid, and the height dict,
    find the shortest way to "E"
    """
    # 1. mark all nodes unvisited: use grid, which contains all nodes in dict
    unvisited = grid.copy()
    # 2. create a dict of {coord: dist}, and initialize all dist to some
    # arbitrary large value
    # also acts as set of visited nodes
    visited = defaultdict(lambda: 1000000)
    visited[root_pos] = 0
    current = root_pos
    # 4. remove current from unvisited set
    # 5. if target is found, exit
    while unvisited:
        # 6. set as current the unvisited node marked with smallest tentative dist
        current = sorted(unvisited, key=lambda k: visited[k])[0]
        letter = unvisited.pop(current)
        #        if letter == "S": # for part one
        #            break
        logger.debug("------------------")
        print(
            f"\rcurrent node and dist: {current}, {visited[current]}",
            sep=" ",
            end=" ",
            flush=True,
        )
        #         print(f"\tlen of visited nodes: {len(visited)}\tunvisited: {len(unvisited)}", sep=" ", end=" ", flush=True)
        logger.debug(f"virgin nodes: {len(unvisited)}")
        # 3. consider all children of current node
        #    if new distance is smaller, update the distance
        candidate_coords = [
            child
            for way in [-1, 1, +1j, -1j]
            if ((child := current + way) in unvisited)
            and (get_height(child) - get_height(current) >= -1)
        ]
        logger.debug(f"candidates: {candidate_coords}")
        logger.debug(
            f"candidate heights: {[get_height(c) - get_height(current) for c in candidate_coords]}"
        )
        dist = visited[current] + 1
        for coord in candidate_coords:
            if dist < visited[coord]:
                visited[coord] = dist

    return current, visited[current], visited


def get_height(coord: complex) -> int:
    """
    Use `ord()` to return int rep of string char
    Replaces 'S' with 'a' and 'E' with 'z'
    """
    ch = grid.get(coord, "{")
    ch = ch.replace("S", "a").replace("E", "z")
    return ord(ch) - ord("a")


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
    grid = open(fp).read().replace("\n", "")
    width = len(next(load_input(fp)))
    logger.debug(f"width: {width}")
    # build dict to use grid.get(complex_coord) and bypass the need for
    # integer list indices
    grid = {get_coord(x, width): grid[x] for x in range(len(grid))}
    logger.debug(f"{[item for item in grid]}")
    print(f"grid size: {len(grid)}")
    src = [coord for coord in grid if grid[coord] == "E"][0]
    print(f"source coord: {src}")
    top, dist, visited = path_find(src, grid)
    print("E found")
    logger.debug(f"E coord: {top}")
    print(f"shortest distance: {dist}")
    shortest = min(
        [
            visited[node]
            for node in visited
            if (grid[node] == "a") or (grid[node] == "S")
        ]
    )
    print(f"part two: {shortest}")
