#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
from dataclasses import dataclass

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

# @dataclass
class Cnode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None
    def __repr__(self) -> str:
        return f'val: {self.val}; next: {self.next.val}'

def create_circ_list(lines):
    head = Cnode(int(next(lines)))
    prev = head
    leng = 1
    for line in lines:
        curr = Cnode(int(line))
        prev.next = curr
        prev = curr
        leng += 1

    # full circle
    curr.next = head
    return head, leng

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
    # order = [int(line) for line in read_line(fp) if line.strip()]
    # order = [Cnode(int(line)) for line in read_line(fp) if line.strip()]
    head, leng = create_circ_list(read_line(fp))

    idx = 0
    curr = head
    while idx < leng:
        logger.debug(f'node: {curr}')
        curr = curr.next
        idx += 1
    logger.info(f'len: {leng}')
    
    # execute
    tstart = time_ns()
    milestone = leng // 100
    circular = order.copy()
    for i, num in enumerate(order):
        if i > milestone:
            # logger.info(f'processing {i+1} / {leng}')
            milestone += milestone
        if num == 0:
            continue
        idx = circular.index(num)
        chk_idx = idx + num
        if chk_idx > leng:
            # how to handle multiple wrappings???
            chk_idx = chk_idx % leng + 1
            circular = circular[:chk_idx]  + [num] + circular[chk_idx: idx] + circular[idx+1:]
        else:
            if chk_idx < 0:
                chk_idx -= 1
            elif chk_idx == 0:
                chk_idx = leng - 1
            elif chk_idx == leng - 1:
                chk_idx = 0
            circular = circular[:idx] + circular[idx + 1: chk_idx+1] + [num] + circular[chk_idx+1:]
        
        # if idx < chk_idx:
        # else:
        #     circular = circular[:chk_idx] + circular[chk_idx + 1: idx] + [num] + circular[idx+1:]
        logger.debug(f'moved {num} to between {circular[chk_idx-1]} and {circular[chk_idx+1]}\nseq: {circular}')

    z_idx = circular.index(0)
    groves = [(coord_idx % leng + z_idx) % leng for coord_idx in [1000, 2000, 3000]]
    # output
    logger.info(f'sum: {sum(groves)}')
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
