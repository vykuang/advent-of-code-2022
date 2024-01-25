#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
from itertools import combinations
from dataclasses import dataclass

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
    cubes = [Cube(*(map(int, line.split(',')))) for line in read_line(fp)]
    logger.debug(f'cubes:\n{cubes}')

    # execute
    tstart = time_ns()
    # check for adjacencies between each pair
    adj = [c1.check_adjacent(c2) for c1, c2 in combinations(cubes, 2)]
    sa = len(cubes) * 6 - 2 * sum(adj)

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
