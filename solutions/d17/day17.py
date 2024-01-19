#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
from itertools import cycle

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

bar = (i + 0j for i in range(4))
cross = (1j, 1+1j, 2+1j, 1+0j, 1+2j)
ell = (0j, 1, 2, 2+1j, 2+2j)
eye = (i*1j for i in range(4))
square = (0j, 1, 1j, 1+1j)

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
    # execute
    tstart = time_ns()
    cycle = (bar, cross, ell, eye, square)
    # output
    n_cycle = 0
    limit = 23
    while n_cycle < limit:


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
