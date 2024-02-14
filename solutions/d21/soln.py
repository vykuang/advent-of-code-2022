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

def find_monkey(monkeys: dict, name: str):
    """
    Given the name of monkey, find their value,
    whether it is a int or result of operation
    Assumes the initial 
    """
    # base case - int literal
    # logger.debug(f'monkey: {name}\tjob: {monkeys[name]}')
    if monkeys[name].isnumeric() or monkeys[name][0] == '-':
        logger.debug('int; returning')
        return int(monkeys[name])
    # recursive case - search name until int, and return op
    else:
        logger.debug('job; recursing')
        mka, op, mkb = monkeys[name].split()
        va = find_monkey(monkeys, mka)
        vb = find_monkey(monkeys, mkb)
        return eval(f'va {op} vb')


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
    if part_two:
        # modify to equality check
        a, _, b = monkeys['root'].split()
        monkeys['root'] = ' '.join([a, '==', b])
    logger.debug(f'monkeys: {monkeys}')
    # execute
    tstart = time_ns()
    if part_two:
        humn = 9998
        while not find_monkey(monkeys, 'root'):
            humn += 1
            monkeys['humn'] = str(humn)
        logger.info(f'humn yells {humn}')
    else:
        root = find_monkey(monkeys, 'root')
        logger.info(f'root yells {root}')

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
