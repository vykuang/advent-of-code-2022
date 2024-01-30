#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
from itertools import cycle
from operator import attrgetter
from collections import namedtuple, deque

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

State = namedtuple('State', 'height_inc, pc_idx, jet_idx, tops')

bar = [i + 0j for i in range(4)]
cross = [1j, 2+1j, 1+0j, 1+2j]
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

    shapes: tuple[complex]
        set of coords representing the shape
    jets: int, {-1, 1}
    stacked: set[complex]
        collection of stacked blocks coords
    
    Returns:
    peak: int

    """
    # f = input()
    pc_idx, pc = next(shapes)
    origin = 2 + peak * 1j + 4j
    pos_pc = [origin + part for part in pc]
    peak_pc = max(pos.imag for pos in pos_pc)
    logger.debug(f'pc: {pc}\tpos: {pos_pc}\tdrop point: {peak_pc}')
    while True:
        # drop block until intersection with stacked
        jet_idx, jet = next(jets)
        pushed = [jet + part for part in pos_pc]
        if stacked.isdisjoint(pushed) and min(pushed, key=attrgetter('real')).real >= 0 and max(pushed, key=attrgetter('real')).real < 7:
            # collision and bounds check
            pos_pc = pushed
            # push_msg = 'left' if jet == -1 else 'right'
            # logger.debug(push_msg)
        fell = [part - 1j for part in pos_pc]
        if stacked.isdisjoint(fell) and min(fell, key=attrgetter('imag')).imag >= 0:
            pos_pc = fell
            peak_pc -= 1
            logger.debug('fell')
        else:
            stacked.update(pos_pc)
            # retrieve top profile for hashing
            logger.debug('stopped')
            break
    height_inc = peak_pc - peak if peak_pc > peak else 0
    peak = max(peak, peak_pc)
    logger.debug(f'new peak: {peak}')
    stacked = find_top_profile(stacked, peak)
    tops = tuple([complex(part.real, peak - part.imag) for part in tuple(stacked)])
    # logger.debug(f'tops: {tops}')
    # logger.debug(f'stack: {stacked}')
    return peak, stacked, State(height_inc, pc_idx, jet_idx, tops)


def find_top_profile(stacked: set, peak: int):
    """
    Use flood fill to find the top profile of stack
    """
    new_stack = set()
    visited = set()
    # start from one row above top, from the middle
    src = 3 + (peak + 1) * 1j
    todo = deque([src])
    while todo:
        node = todo.popleft()
        for direc in [-1,1,1j,-1j]:
            child = node + direc
            if child in stacked:
                new_stack.add(child)
            elif child not in visited and 0 <= child.real < 7 and child.imag <= peak + 1:
                todo.append(child)
            else:
                continue
        visited.add(node)
    return new_stack

def draw_stack(peak: int, stacked: set):
    lines = []
    for row in range(peak, 0, -1):
        line = ''.join(['#' if node in stacked else '.' for node in [col + row * 1j for col in range(7)]])
        lines.append(line)
    return lines

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
    # enumerate creates index
    shapes = cycle(enumerate([bar, cross, ell, eye, square]))
    # only 1 line of jets
    jets =  next(read_line(fp))
    jets = [jet_dir[jet] for jet in jets.strip()]
    logger.info(f'length: {len(jets)}')
    if part_two:
        limit = 1000000000000 # 1 tril
        # limit = 5 * len(jets) # len is a prime 
    else:
        limit = 2022
    # execute
    tstart = time_ns()
    jets = cycle(enumerate(jets))
    # initialize the floor
    stacked = set([i + 0j for i in range(7)])
    peak = 0
    ndrops = 0
    height_incs = []
    states = {}
    if part_two:
        # state = [height_inc, shape_idx, jet_idx]
        while True:
            peak, stacked, state = drop_block(jets=jets, shapes=shapes, stacked=stacked, peak=peak)
            ndrops += 1
            if state in states:
                logger.info(f'repeat found @ {ndrops}th drop')
                # start recording height_inc for replay
                break
            if ndrops > 52:
                break
            height_incs.append(state.height_inc)
            states[state] = ndrops
        mu = states[state]
        lam = ndrops - mu
        height_inc_per_cycle = sum(height_incs[mu:])
        logger.info(f'state: {state}\tfirst: {mu}\tlam: {lam}')
        h_precycle = sum(height_incs[:mu])
        ncycles = (limit - mu) // lam
        remainder = (limit - mu) - lam * ncycles
        height_remainder = sum(height_incs[mu:remainder])
        logger.info(f'precycle: {h_precycle}\nncycles: {ncycles}\nh per c: {height_inc_per_cycle}\nh remainder: {height_remainder}')
        peak = h_precycle + ncycles * height_inc_per_cycle + height_remainder

    else:
        for _ in range(limit):
            #f = input()
            peak, stacked, _ = drop_block(jets=jets, shapes=shapes, stacked=stacked, peak=peak)
            # output
            logger.debug(f'current: {peak}')
            # for line in draw_stack(int(peak), stacked):
                # print(line)
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
