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
from functools import reduce

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

@dataclass
class Valve:
    rate: int
    neighbors: list
    opened: bool = False
    duration: int = 0

    def __hash__(self):
        return hash((self.rate, self.neighbors))

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
    name, *neighbors = re.findall(r'[A-Z]{2}', line)
    rate = int(re.findall(r'rate=(\d+)', line)[0])
    return name, Valve(rate, neighbors)

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
    dists[0].append(root)
    visited = set()
    while dists:
        min_cost = min(dists.keys())
        next_caves = dists.pop(min_cost)
        for cave in next_caves:
            if cave == target:
                return min_cost
            if cave in visited:
                continue
            for adj in valves[cave].neighbors:
                if adj not in visited:
                    dists[min_cost + 1].append(adj)

    return None

def find_paths(working_valves: set, dists: dict, root: str = 'AA', time_lim: int = 30, elephant: bool = False):
    """
    Look for all possible paths through the caves within the time limit
    """
    # logger.debug(f'working valves: {working_valves}')
    path = [(root, 0)]
    if root in working_valves:
        working_valves.discard(root)
    time_remain = time_lim
    # what valve to open next?
    yield from find_cave(path, time_remain, working_valves, dists)

def find_cave(path: list, time_remain: int, working_valves: set, dists: dict):
    """
    Recursively find the next cave, until time limit is met
    """
    for cave in working_valves:
        # f = input()
        time_req = dists[path[-1][0]][cave] + 1
        # logger.debug(f'from {path[-1][0]} checking {cave}; req: {time_req}')
        if time_remain <= time_req:
            # yield if time's up
            # logger.debug(f'times up: {path}')
            yield path
        else:
            alt_time_remain = time_remain - time_req
            new_pool = working_valves.copy()
            new_pool.discard(cave)
            if new_pool:
                # logger.debug(f'enough time; {alt_time_remain} left\nchoosing from {new_pool}')
                yield from find_cave(path + [(cave, alt_time_remain)], alt_time_remain, new_pool, dists)
            else:
                # empty pool; all nodes visited
                yield path + [(cave, alt_time_remain)]

def find_cave_elephant(paths: list, time_remains: list, working_valves: set, dists: dict):
    """
    Now there's an elephant
    Two paths, with their own timer
    Each call adds one valve to path, until timer runs out
    Recursion ends when both path timer runs out
    """
    for cave in working_valves:
        # try each valve on human path
        time_req = dists[paths[0][-1][0]][cave] + 1
        if time_remains[0] <= time_req:
            # time's up for human path
            pass
        else:
            h_next = (cave, time_remains[0] - time_req)
            e_pool = working_valves.copy()
            e_pool.discard(cave)
            for cave in e_pool:
                time_req = dists[paths[1][-1][0][cave] + 1
                    if time_remains[1] <= time_req:
                    # time's up for elephant
                        yield paths #???
                    else:
                        e_next = (cave, time_remains[1] - time_req)
                        paths[0].append(h_next)
                        paths[1].append(e_next)
                        time_remains[0].append(h_next[1])
                        time_remains[1].append(e_next[1])
                        if e_pool:
                            yield from find_cave_elephant(
                                paths,
                                time_remains,
                                e_pool,
                                dists)
                        else:
                            
                                









    while working_valves:
        for path, time_remain in zip(paths, time_remains):
            cave = working_valves.pop()
            time_req = dists[path[-1][0]][cave] + 1
            if time_remain <= time_req:
                # time's up
                next
            else:
                # append to path 
                path += (cave, time_remain)




def calc_pressure(tunnel: list[tuple], valves: dict) -> int:
    """
    Given tuple of ('VALVE_ID', time_remain), calculate
    pressure released
    """
    logger.debug(f'tunnel: {tunnel}')
    pressures = [valves[v[0]].rate * v[1] for v in tunnel]
    return sum(pressures)

def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if sample:
        fp = "sample.txt"
    else:
        fp = "input.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')
    
    if part_two:
        time_lim = 26
    else:
        time_lim = 30
    # read input
    valves = {v[0]: v[1] for line in read_line(fp) if (v := parse_valve_tunnel(line.strip()))}
    # execute
    tstart = time_ns()
    # find shortest paths between all valves
    working_valves = {name for name, v in valves.items() if v.rate or name == 'AA'}
    dists = defaultdict(dict)
    for root, target in combinations(working_valves, 2):
        shortest = dijkstra_valves(valves, root, target)
        dists[root][target] = shortest
        # double sided dict
        dists[target][root] = shortest

    # given shortest paths between all *working* valves, plus src, find optimal path
    # within the time limit
    # sums = []
    # for tunnel in find_paths(working_valves, dists, 'AA', time_lim):
        # logger.debug(f'tunnel: {tunnel}')
        # tunnel format: [(valve, time_remain), ..., (valve_n, time_remain_0)]
        # look for rate, multiply by time, sum the tuples
        # sums.append(reduce(lambda x, y: x + valves[y[0]].rate * y[1], tunnel, 0))
    human_paths = [(tunnel, calc_pressure(tunnel, valves))
            for tunnel in find_paths(working_valves, dists, 'AA', time_lim)]
    if part_two:
        elephant_valve_pools = [working_valves.difference([t[0] for t in path[0]]) for path in human_paths]
        logger.debug('elephant pools:\n')
        for pool in elephant_valve_pools:
            logger.debug(f'{pool}')
            

    # output
    # logger.debug(f'dists:\n{dists}')
    logger.info(f'max release: {max(human_paths, key=lambda t: t[1])}')
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
