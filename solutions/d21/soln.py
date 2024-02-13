#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def parse_monkey(line: str):
    """
    format:
        name: mnk1 <op> mnk2
        or,
        name: <int>
    return as name, op
    """
    return line.strip().split(':')

def find_monkey(name):
    """
    Given the name of monkey, find their value,
    whether it is a int or result of operation
    """

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
    monkeys = {l[0].strip(): l[1].strip() for line in read_line(fp) if (l := parse_monkey(line))}
    logger.debug(f'monkeys: {monkeys}')
    # execute
    tstart = time_ns()
    for monkey, job in monkeys.items():
        if job.isnumeric():
            seen[monkey] = int(job)
        else:
            op1, op, op2 = job.split()

    # output

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
