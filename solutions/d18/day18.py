#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
from itertools import combinations
from dataclasses import dataclass
from operator import attrgetter

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

def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample2.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    cubes = [Cube(*(map(int, line.split(',')))) for line in read_line(fp)]
    logger.debug(f'cubes:\n{cubes}')

    # execute
    tstart = time_ns()
    # check for adjacencies between each pair
    adj = [c1.check_adjacent(c2) for c1, c2 in combinations(cubes, 2)]
    sa = len(cubes) * 6 - 2 * sum(adj)
    if part_two:
        # zsort = sorted(cubes, key=getattr('z'))
        # zmin = zsort[0].z
        # zmax = zsort[-1].z
        pockets = []
        zmin, zmax = find_min_max(cubes, 'z')
        for z in range(zmin + 1, zmax):
            ymin, ymax = find_min_max(cubes, 'y')
            for y in range(ymin + 1, ymax):
                xmin, xmax = find_min_max(cubes, 'x')
                for x in range(xmin + 1, xmax):
                    # look for air pockets
                    if (pocket := Cube(x, y, z)) not in cubes:
                        logger.debug(f'pocket: {pocket}')
                        pockets.append(pocket)
        pockets_adj = [p1.check_adjacent(p2) for p1, p2 in combinations(pockets, 2)]
        psa = 6 * len(pockets) - 2 * sum(pockets_adj)
        logger.info(f'droplet total sa: {sa}\npockets sa: {psa}')
        sa -= psa

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
