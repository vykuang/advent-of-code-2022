#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
import re
from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

@dataclass
class Valve:
    rate: int = 0
    neighbors: list = []
    opened: bool = False

    def __hash__(self):
        return hash((rate, neighbors))

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f


def parse_valve_tunnel(line: str) -> list:
    """Parse input to return 
    - valve name: str
    - rate: int
    - neighbors: list[str]
    in the form of a Valve object
    """
    v = re.compile('[A-Z]{2}')
    r = re.compile('rate=(\d+)')
    name, *neighbors = v.findall(line)
    rate = int(r.findall(line)[0])
    return name, rate, neighbors

def dijkstra_valves(valves, root, target):
    """
    valves: dict
        contains Valve objects, with rate and neighbors attr
    root, target: str
        name of valves; keys for valves dict
    returns shortest distances between every pair of caves
    """
    # distance act as keys; caves are the values
    dists = defaultdict(list)
    dists[0] = root
    visited = set()
    while dists:
        min_cost = min(dists.keys())
        next_caves = dists.pop(min_cost)
        for cave in next_caves:
            if cave == target:
                return min_cost
            if cave in visited:
                continue
            for adj in cave.neighbors:
                if adj not in visited:
                    dists[min_cost + 1].append(adj)


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
    valves = {v[0]: Valve(v[1], v[2]) for line in read_line(fp) if (v := parse_valve_tunnel(line))}
    # execute
    tstart = time_ns()
    # find shortest paths between all valves
    working_valves = {v for v in valves if v.rate}
    dists = defaultdict(dict)
    for root, target in combinations(valves):
        dists[root][target] = dijkstra_valves(valves, root, target)
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
