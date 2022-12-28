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

def draw_pixel(cycle: int, val: int, period: int = 40) -> str:
    """Determine which pixel to draw by judging cycle and val
    Returns the correct pixel
    """
    pos = (cycle - 1) % period
    if (abs(pos - val) == 1) | (pos == val): 
        return "#"
    else:
        return "."

if __name__ == "__main__":
    fn = sys.argv[1]
    match fn:
        case "test" | "input":
            fp = f"{fn}.txt"
            test = fn == "test" 
        case _:
            raise ValueError(f"{fn} cannot be used")
            
    if test:
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
    else:
        logger.setLevel(logging.INFO)
    PERIOD = 40
    FIRST_PERIOD = 20
    cycle = 1
    val = 1
    sigs = []
    row = ""
    for line in load_input(fp):
        logger.info(f"============")
        logger.info(f"executing {line}")
        # drawing occurs before the line instruction complete
        row += draw_pixel(cycle, val)
        pos = (cycle - 1) % PERIOD
        logger.info(f"cycle {cycle}; val: {val}; pos: {pos}\nadd: {row[-1]}")
        match line.split(" "):
            case ["noop"]:
                cycle += 1

            case ["addx", arg]:
                # check for edge cases here
                if (cycle - FIRST_PERIOD) % PERIOD == PERIOD - 1 or cycle == FIRST_PERIOD-1:
                    logger.debug("SIGNAL STRENGTH COLLECTED")
                    sigs.append((1+cycle)* val)
                # part two
                # draw additional pixel for the extra cycle addv takes
                cycle += 1
                row += draw_pixel(cycle, val)
                pos = (cycle - 1) % PERIOD
                logger.info(f"cycle {cycle}; val: {val}; pos: {pos}\nadd: {row[-1]}")
                val += int(arg)
                cycle += 1
        # general case
        if (cycle - FIRST_PERIOD) % PERIOD == 0 or cycle == FIRST_PERIOD:
            logger.debug("SIGNAL STRENGTH COLLECTED")
            sigs.append(cycle * val)
        logger.debug(f"cycle after inst: {cycle}\treg:{val}")


    print(f"signal strength collected:\t{sigs}")
    print(f"sum: {sum(sigs)}")

    for i in range(0, len(row), PERIOD):
        print(row[i:i+PERIOD])

