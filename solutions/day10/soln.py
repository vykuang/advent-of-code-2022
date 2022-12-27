#! /usr/bin/env python
"""
AoC 2022 Day
"""

import sys
import logging

logger = logging.getLogger(__name__)

def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

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
    PERIOD = 40
    FIRST_PERIOD = 20
    cycle = 1
    val = 1
    sigs = []
    rows = []
    for line in load_input(fp):
        logger.debug(f"============")
        logger.debug(f"line: {line}")
        match line.split(" "):
            case ["noop"]:
                cycle += 1
            case ["addx", arg]:
                # check for edge cases here
                if (cycle - FIRST_PERIOD) % PERIOD == PERIOD - 1 or cycle == FIRST_PERIOD-1:
                    logger.debug("SIGNAL STRENGTH COLLECTED")
                    sigs.append((1+cycle)* val)
                cycle += 2
                val += int(arg)
        # general case
        if (cycle - FIRST_PERIOD) % PERIOD == 0 or cycle == FIRST_PERIOD:
            logger.debug("SIGNAL STRENGTH COLLECTED")
            sigs.append(cycle * val)
        logger.debug(f"cycle after inst: {cycle}\treg:{val}")

    print(f"signal strength collected:\t{sigs}")
    print(f"sum: {sum(sigs)}")
    for row in rows:
        print(row)
