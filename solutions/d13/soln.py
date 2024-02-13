#! /usr/bin/env python
"""
AoC 2022 Day
"""

import sys
import logging

logger = logging.getLogger(__name__)


def cmp(left: int | list, right: int | list):
    """
    Recursively compares the two packets
    Most cases will start with comparing list to list
    and end with int-int
    """
    logger.debug(f"left: {left}\tright: {right}")
    match left, right:
        case int(), int():
            logger.debug("int-int")
            # this gives us three states: <, ==, or >
            # use the returned sign to determine
            # whether packets are equal
            return left - right
        case int(), list():
            logger.debug("int-list")
            return cmp([left], right)
        case list(), int():
            logger.debug("list-int")
            return cmp(left, [right])
        case list(), list():
            logger.debug("list-list")
            for z in map(cmp, left, right):
                if z:  # any value besides 0
                    return z
            # if checks whether one list runs out
            # if so, compare the lengths of the lists
            return cmp(len(left), len(right))


if __name__ == "__main__":
    fn = sys.argv[1]
    match fn:
        case "test" | "input":
            fp = f"{fn}.txt"
            test = fn == "test"
        case _:
            raise ValueError(f"{fn} cannot be used")

    if test:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
    else:
        logger.setLevel(logging.INFO)

    with open(fp) as f_in:
        puzzle = f_in.read()

    # split by \n\n to get the pairs that are sep'd by blank line
    # line.split() separates the packets in the pair
    # map(eval, line.split()) performs eval() on each
    # packet in the pair
    # *map() unpacks the map object into actual objects
    # which in this case are the results of eval()
    packets = [[*map(eval, line.split())] for line in puzzle.split("\n\n")]
    pair_sum = 0
    for i, pkt in enumerate(packets, start=1):
        logger.debug(f"pkt: {pkt}")
        if cmp(*pkt) < 0:
            pair_sum += i
            logger.debug(f"packet in order. current sum: {pair_sum}")
    print(f"part i sum: {pair_sum}")

    all_pkts = [eval(line) for line in puzzle.split()]
    logger.debug(f"part two ---------\n{all_pkts}")
    cmp_res = [cmp([[2]], line) for line in all_pkts]
    logger.debug(f"comparison results to [[2]]:\n{cmp_res}")
    above_first_div = len([z for z in cmp_res if z > 0])
    print(f"num pkts above [[2]]: {above_first_div}")
    cmp_res2 = [cmp([[6]], line) for line in all_pkts]
    ab_sec_div = len([z for z in cmp_res2 if z > 0])
    print(f"num pkts above [[6]]: {ab_sec_div}")
    decoder = (above_first_div + 1) * (ab_sec_div + 2)
    print(f"decoder: {decoder}")
