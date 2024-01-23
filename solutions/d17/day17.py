#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
from itertools import cycle
from operator import attrgetter

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

bar = [i + 0j for i in range(4)]
cross = [1j, 1+1j, 2+1j, 1+0j, 1+2j]
ell = [0j, 1, 2, 2+1j, 2+2j]
eye = [i*1j for i in range(4)]
square = [0j, 1, 1j, 1+1j]

jet_dir = {'<': -1, '>': 1}

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
    shapes = cycle([bar, cross, ell, eye, square])
    jets =  next(read_line(fp))
    jets = [jet_dir[jet] for jet in jets.strip()]
    logger.debug(f'jets pattern: {jets}')
    jets = cycle(jets)
    # execute
    tstart = time_ns()

    limit = 2022
    stacked = set([i + 0j for i in range(7)])
    for pcount in range(limit):
        pc = next(shapes)
        origin = 2 + max(stacked, key=attrgetter('imag')).imag * 1j + 4j
        pos_pc = [origin + part for part in pc]
        bottom = False
        logger.debug(f'pc: {pc}\nstart pos: {pos_pc}')
        while not bottom:
            # apply jets first
            jet = next(jets)
            pushed = [jet + part for part in pos_pc]
            if stacked.isdisjoint(pushed) and min(pushed, key=attrgetter('real')).real >= 0 and max(pushed, key=attrgetter('real')).real < 7:
                pos_pc = pushed
                logger.debug(f'pushed: {pushed}')
            # fall down 1 unit
            fell = [part - 1j for part in pos_pc]
            if stacked.isdisjoint(fell) and min(fell, key=attrgetter('imag')).imag >= 0:
                pos_pc = fell
                logger.debug(f'fell: {fell}')
            else:
                bottom = True
                stacked.update(pos_pc)
                logger.debug(f'stopped at {pos_pc}')

    height = max(stacked, key=attrgetter('imag')).imag


    # output
    logger.info(f'height: {height}')


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
