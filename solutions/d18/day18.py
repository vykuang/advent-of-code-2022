#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
from dataclasses import dataclass
from operator import attrgetter
from collections import deque

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

@dataclass
class Cube:
    x: int
    y: int
    z: int

    def check_adjacent(self, cube2):
        # comp_check = [getattr(self, comp) == getattr(cube2, comp) for comp in Cube.__annotations__.keys()]
        # if sum(comp_check) == 2:
        #     c1_comp = 
        n_share = 0
        possible_adj = False

        for comp in Cube.__annotations__.keys():
            # cycle through attr x, y, z 
            if (comp1 := getattr(self, comp)) == (comp2 := getattr(cube2, comp)):
                n_share += 1
            else:
                if abs(comp1 - comp2) == 1:
                    # check the comp that's different
                    possible_adj = True
        if n_share == 2 and possible_adj:
            return True
        else:
            return False
        
    def sides(self) -> list:
        east = Cube(self.x + 1, self.y, self.z)
        west = Cube(self.x - 1, self.y, self.z)
        north = Cube(self.x, self.y+1, self.z)
        south = Cube(self.x, self.y-1, self.z)
        out = Cube(self.x, self.y, self.z+1)
        into = Cube(self.x, self.y, self.z-1)
        return {east, west, north, south, out, into}
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __repr__(self) -> str:
        return f'Cube({self.x}, {self.y}, {self.z})'

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def find_min_max(cubes, comp):
    """
    Given list of cubes, find the min and max of the specified component
    """
    if comp not in Cube.__annotations__.keys():
        return
    csort = sorted(cubes, key=attrgetter(comp))
    cmin = getattr(csort[0], comp)
    cmax = getattr(csort[-1], comp)
    return cmin, cmax

def is_in_boundary(cube, zmin, zmax, ymin, ymax, xmin, xmax):
    return zmin -1 <= cube.z <= zmax + 1 and ymin - 1 <= cube.y <= ymax + 1 and xmin - 1 <= cube.x <= xmax + 1

def flood_fill(cubes: set):
    """
    Use flood fill to find external surface area of this set of cubes
    """
    zmin, zmax = find_min_max(cubes, 'z')
    ymin, ymax = find_min_max(cubes, 'y')
    xmin, xmax = find_min_max(cubes, 'x')
    src = Cube(xmin-1, ymin-1, zmin-1)
    logger.debug(f'starting from {src}\tboundary @ {xmax}, {ymax}, {zmax}')

    todo = deque([src])
    visited = set()
    ext_sa = 0
    while todo:
        cube = todo.popleft()
        # check if part of droplet
        if cube in visited:
            continue
        if cube in cubes:
            ext_sa += 1
            logger.debug(f'surface reached @ {cube}\tcurrent sa: {ext_sa}')
            continue
        # check if cube is inside bounds, but not part of droplet
        elif is_in_boundary(cube, zmin, zmax, ymin, ymax, xmin, xmax):
            # add other 6 dirs to queue
            for side in cube.sides():
                if side not in visited and is_in_boundary(side, zmin, zmax, ymin, ymax, xmin, xmax):
                    todo.append(side)
            visited.add(cube)
        else:
            continue
    return ext_sa


def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    cubes = {Cube(*(map(int, line.split(',')))) for line in read_line(fp)}
    logger.debug(f'cubes:\n{cubes}')

    # execute
    tstart = time_ns()
    if part_two:
        # exterior flood fill
        sa = flood_fill(cubes)
    else:
        # count sides exposed to air
        sa = sum([len(cube.sides() - cubes) for cube in cubes])
    # output
    logger.info(f'surface area: {sa}')
    tstop = time_ns()
    logger.info(f"runtime: {(tstop-tstart)/1e6} ms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    opt = parser.add_argument
    opt("--sample", "-s", action="store_true", default=False)
    opt("--part_two", "-t", action="store_true", default=False)
    opt("--loglevel", "-l", type=str.upper, default="info")
    args = parser.parse_args()
    main(args.sample, args.part_two, args.loglevel)
