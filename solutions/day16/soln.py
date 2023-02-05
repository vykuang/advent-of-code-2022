#! /usr/bin/env python
"""
AoC 2022 Day
"""

import sys
import logging
from collections import defaultdict
import re
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()


def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

def parse_valve_tunnel(line: str) -> list:
    """Parse input to return 
    - valve name: str
    - rate: int
    - children: list[str]
    """
    v = re.compile('[A-Z]{2}')
    r = re.compile('rate=(\d+)')
    v_m = v.findall(line)
    r_m = r.findall(line)
    return v_m[0], int(r_m[0]), v_m[1:]

class Valve:
    def __init__(self, rate=0, neighbors=None):
        """To use in defaultdict, must set defaults"""
        self.rate = rate
        if neighbors:
            self.neighbors = set(neighbors)
        else:
            self.neighbors = None
        
    def __repr__(self):
        return f"rate: {self.rate}\tneighbors: {self.neighbors}"

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

    tunnels = defaultdict(Valve)
    for line in load_input(fp):
        name, rate, neighbors = parse_valve_tunnel(line)
        tunnels[name] = Valve(rate, neighbors)
