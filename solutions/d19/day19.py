#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
import re
# from dataclasses import dataclass
from collections import defaultdict
from math import inf, isinf
from functools import cache

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

paths = 0

class Hashabledict(dict):
    def __hash__(self) -> int:
        return hash(frozenset(self))
    
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
    # logger.debug(f'req: {req}')
    if not req:
        return
    parts = re.findall(r'.*(ore|clay|obsidian|geode).*costs (\d+) (ore|clay|obsidian)(?: and (\d+) (ore|clay|obsidian))*', req)[0]
    # logger.debug(f'parts: {parts}')
    robot = parts[0][:3]
    i = 1
    reqs = Hashabledict()
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
    # logger.debug(f'bid: {bid}\nraw reqs: {reqs}')
    blueprint = {p[0]: p[1] for req in reqs.split('.') if (p := parse_req(req.strip()))}
    return bid, Hashabledict(blueprint)

def not_find_geodes(bp: dict, timelim: int = 24) -> int:
    """
    Find geodes given blueprint
    Rules are hardcoded, and will not find max n_geo
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

@cache
def max_mat_req(t_remain: int, mat: str, blueprint: Hashabledict) -> int:
    """
    Given t_remain, material, and blueprint,
    calculate the max number of mat needed if that robot
    was built for all remaining minutes
    """
    # find highest req of this material
    reqs = [req for robot in blueprint.values() if (req := robot.get(mat))]
    if reqs:
        return t_remain * max(reqs)


def find_geodes(nmats, rates, t_remain, blueprint, skipped=[]):
    """
    Given nmat, rates, t_remain, use tree search
    to maximize nmats['geo']
    Params
    --------
    skipped: list
        robots that could have been built last minute but was not
    """
    logger.debug(f'======== minute {t_remain} ========\nmats: {nmats}\nrates: {rates}')
    if t_remain == 1:
        ngeos = nmats['geo'] + rates['geo']
        # lets python know this is the global scope var, before it looks
        # for a local `paths`
        global paths
        paths += 1
        if ngeos > 0:
            logger.debug(f"times up, collected {ngeos} geodes")
        return ngeos
    # check resources
    build = {}
    for robot in nmats:
        if isinf(nmats[robot]):
            # no point checking for robot req and collecting if more than enough
            continue
        # enable build, but do not build yet
        if all(nmats[req] >= blueprint[robot][req] for req in blueprint[robot]):
            logger.debug(f'enough to build {robot} robot')
            build[robot] = True
        # collect ores after enabling build
        nmats[robot] += rates[robot]
        # check if we have more than enough
        if robot != 'geo' and nmats[robot] >= max_mat_req(t_remain - 1, robot, blueprint):
            logger.debug(f'maxed resource {robot}')
            nmats[robot] == inf
    logger.debug(f'after collection:\n{nmats}')
    t_remain -= 1
    for robot in build:
        # can only build one robot at a time
        if build[robot] and robot not in skipped:
            # spend resources
            new_mats = nmats.copy()
            new_mats.update({req: nmats[req] - blueprint[robot][req] for req in blueprint[robot]})
            new_rates = rates.copy()
            new_rates[robot] += 1
            logger.debug(f'after building {robot} robot:\nmats: {new_mats}\nrates: {new_rates}')
            # next minute will not build all other robots
            skipped = [b for b in build if b != robot]
            yield from find_geodes(new_mats, new_rates, t_remain, blueprint, skipped)

    # paths that do not build
    yield from find_geodes(nmats, rates, t_remain, blueprint)


def main(sample: bool, part_two: bool, loglevel: str, t_limit=24):
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
    global paths
    # execute
    tstart = time_ns()
    mats = ['geo', 'obs', 'cla', 'ore']
    # for each blueprint:
    #   simulate minute by minute, starting with 1 ore collector
    #   initialize all other collector rates to 0
    nmats = dict(zip(mats, [0] * 4))
    rates = dict(zip(mats, [0,0,0,1]))
    # qlevels = [find_geodes(nmats=nmats,rates=rates,t_remain=t_limit,blueprint=bp) for bp in blueprints.values()]
    for bp in blueprints.values():
        qs = find_geodes(nmats=nmats,rates=rates,t_remain=t_limit,blueprint=bp)
        for q in qs:
            # logger.info(f'max for bp: {max(q)}') 
            logger.info(f'paths: {paths}')
            paths = 0
            logger.info(f'q: {q}')           
    # output
    logger.info(f'{paths} paths found')
    tstop = time_ns()
    logger.info(f"runtime: {(tstop-tstart)/1e6} ms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    opt = parser.add_argument
    opt("--sample", "-s", action="store_true", default=False)
    opt("--part_two", "-t", action="store_true", default=False)
    opt("--loglevel", "-l", type=str.upper, default="info")
    opt("--time", "-m", type=int)
    args = parser.parse_args()
    main(args.sample, args.part_two, args.loglevel, args.time)
