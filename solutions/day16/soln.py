#! /usr/bin/env python
"""
AoC 2022 Day
"""

import sys
import logging

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()


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
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    logger.setLevel(loglevel)
    ch.setLevel(loglevel)
    logger.addHandler(ch)

    for line in load_input(fp):
        pass
