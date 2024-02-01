#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
import re
# from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

def parse_req(req: str):
    """
    Given 'Each geode robot costs 2 ore and 7 obsidian'
    return {'geo': {'ore': 2, 'obs': 7}}
    """
    logger.debug(f'req: {req}')
    if not req:
        return
    parts = re.findall(r'.*(ore|clay|obsidian|geode).*costs (\d+) (ore|clay|obsidian)(?: and (\d+) (ore|clay|obsidian))*', req)[0]
    logger.debug(f'parts: {parts}')
    robot = parts[0][:3]
    i = 1
    reqs = {}
    while i < len(parts):
        # only keep 1st 3 letters of material type
        if parts[i]:
            reqs[parts[i + 1][:3]] = int(parts[i])
        i += 2
    return robot, reqs


def parse_blueprint(line: str):
    """
    Return parsed blueprints in the form of dict
    e.g. Blueprint 1:  
        Each ore robot costs 4 ore.  
        Each clay robot costs 2 ore.  
        Each obsidian robot costs 3 ore and 14 clay.  
        Each geode robot costs 2 ore and 7 obsidian.
    {1: {'ore': {'ore': 4}, 'clay': {'ore': 2}, 'obs': {'ore': 3, 'clay': 14},
    'geo': {'ore': 2, 'obs': 7}}}
    """
    bid, reqs = line.split(':')
    bid = int(bid.split()[-1])
    logger.debug(f'bid: {bid}\nraw reqs: {reqs}')
    blueprint = {p[0]: p[1] for req in reqs.split('.') if (p := parse_req(req.strip()))}
    return bid, blueprint

def find_geodes(bp: dict, timelim: int = 24) -> int:
    """
    Find geodes given blueprint
    """
    mats = ['geo', 'obs', 'cla', 'ore']
    rates = defaultdict(lambda: 0)
    rates['ore'] = 1
    nmats = defaultdict(lambda: 0)
    build = defaultdict(lambda: False)
    for t in range(timelim):
        logger.debug(f'== minute {t} ==')
        # spend mats to build; check reqs
        # naive method will always build only clay robots
        # need pathfinding; at each point we have enough,
        # one path builds it, and the other saves it for next round
        for robot in mats:
            logger.debug(f'checking reqs for {robot} robot')
            if all(nmats[mat] >= bp[robot][mat] for mat in bp[robot]):
                build[robot] = True
                logger.debug(f'building {robot} robot')
                for mat in bp[robot]:
                    nmats[mat] -= bp[robot][mat]
                logger.debug(f'mats after consumption:\n{nmats}')

        # collect ores
        for mat in mats:
            nmats[mat] += rates[mat]
            if build[mat]:
                logger.debug(f'rate inc for {mat}')
                rates[mat] += 1
                build[mat] = False
        logger.debug(f'nmats: {nmats}')

        f = input()
    return nmats['geo']

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
    blueprints = {b[0]: b[1] for line in read_line(fp) if (b := parse_blueprint(line))}
    logger.debug(f'bps:\n{blueprints}')

    # execute
    tstart = time_ns()

    # for each blueprint:
    #   simulate minute by minute, starting with 1 ore collector
    #   initialize all other collector rates to 0
    qlevels = [find_geodes(bp) for bp in blueprints.values()]
            
    # output
    logger.info(f'qlevels: {qlevels}')
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
