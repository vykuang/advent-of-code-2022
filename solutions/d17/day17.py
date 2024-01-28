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

def drop_block(shapes, jets, stacked, peak=0) -> int:
    """
    Drops the block onto the stack accounting for jets

    pc: tuple[complex]
        set of coords representing the shape
    jets: int, {-1, 1}
    stacked: set[complex]
        collection of stacked blocks coords
    
    Returns:
    peak: int

    """
    f = input()
    drops = 0
    pc = next(shapes)
    origin = 2 + peak * 1j + 4j
    pos_pc = [origin + part for part in pc]
    peak_pc = max(pos.imag for pos in pos_pc)
    logger.debug(f'pc: {pc}\tpos: {pos_pc}\tpeak: {peak_pc}')
    while True:
        # drop block until intersection with stacked
        jet = next(jets)
        pushed = [jet + part for part in pos_pc]
        if stacked.isdisjoint(pushed) and min(pushed, key=attrgetter('real')).real >= 0 and max(pushed, key=attrgetter('real')).real < 7:
            pos_pc = pushed
            logger.debug('pushed')
        # fall down 1 unit
        fell = [part - 1j for part in pos_pc]
        if stacked.isdisjoint(fell) and min(fell, key=attrgetter('imag')).imag >= 0:
            pos_pc = fell
            drops += 1
            logger.debug('fell')
        else:
            stacked.update(pos_pc)
            logger.debug('stopped')
            break
    logger.debug(f'new peak: {peak_pc} - {drops}')
    return peak_pc - drops 

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
    logger.info(f'length: {len(jets)}')
    if part_two:
        limit = 1000000000000 # 1 tril
    else:
        # limit = len(jets) * 5
        limit = 2022
    # execute
    tstart = time_ns()
    jets = cycle(jets)
    stacked = set([i + 0j for i in range(7)])
    peak = 0
    for _ in range(limit):
            # logger.debug(f'pc: {pc}\nstart pos: {pos_pc}')
        peak += drop_block(jets=jets, shapes=shapes, stacked=stacked, peak=peak)
        # output
        logger.debug(f'current: {peak}')
    logger.info(f'height: {peak}')


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
