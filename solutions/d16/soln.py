#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
import re
from dataclasses import dataclass
from collections import defaultdict
from math import inf

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

@dataclass
class Valve:
    rate: int
    neighbors: list

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

def find_dists(valves, root, target):
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

def find_dists_fw(valves):
    """Floyd-warshall to find shortest paths between all pairs of vertices
    shortest(i, j, k) = 
        min(shortest(i, j, k - 1),
            shortest(i, k, k - 1) + shortest(k, j, k - 1))
    where i, j are nodes, 0 - k represents all intermediate nodes
    base:
    shortest(i, j, 0) = w(i, j), where w is edge weight b/w i, j
    """
    # first build adjacency matrix
    dist = defaultdict(dict)
    for i in valves:
        for j in valves:
            if i == j:
                dist[i][j] = 0
            elif j in valves[i].neighbors:
                dist[i][j] = 1
            else:
                # initialize to inf if not direct neighbor
                dist[i][j] = inf

    # apply f-w algo
    for k in valves:
        for i in valves:
            for j in valves:
                if dist[i][j] > (new_dist := dist[i][k] + dist[k][j]):
                    dist[i][j] = new_dist
    return dist
            

def find_cave(path: list, node, time_remain, working_valves: set, dists: dict):
    """
    Recursively find the next cave, until time limit is met
    """
    if not working_valves or not any([dists[node][cave] + 1 < time_remain for cave in working_valves]):
        # empty pool; all nodes visited, or time's up
        # need to occur prior to non-base case to avoid yielding 
        # intermediate paths
        logger.debug(f'empty or cannot reach {working_valves}; returning path')
        yield path

    for cave in working_valves:
        # f = input()
        cost = dists[node][cave] + 1
        logger.debug(f'{node} -> {cave}; cost: {cost}')
        if cost < time_remain:
            logger.debug(f'enough time; {time_remain - cost} left')
            yield from find_cave(path + [(cave, time_remain - cost)], cave, time_remain - cost, working_valves - {cave}, dists)
            
    

def extract_valves(tunnel: list) -> list:
    """
    Given list of [(id, int), ...],
    extract id and compile into list of [id, id, ...]
    """
    return [v[0] for v in tunnel]


def calc_pressure(tunnel: list[tuple], valves: dict) -> int:
    """
    Given tuple of ('VALVE_ID', time_remain), calculate
    pressure released
    """
    logger.debug(f'tunnel: {tunnel}')
    return sum([valves[v[0]].rate * v[1] for v in tunnel])

def main(sample: bool, part_two: bool, loglevel: str, root=root):
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
    working_valves = {name for name, v in valves.items() if v.rate or name == root}

    # /--------------------dijkstra for each combination ---------------------/
    # dists = defaultdict(dict)
    # for root, target in combinations(working_valves, 2):
    #     shortest = find_dists(valves, root, target)
    #     dists[root][target] = shortest
    #     # double sided dict
    #     dists[target][root] = shortest

    # floyd-warshall; better for dense graphs (each node accessible by all)
    dists = find_dists_fw(valves)
    dists = {i: j for i, j in dists.items() if (valves[i].rate or i == root)}

    # given shortest paths between all *working* valves, plus src, find optimal path
    # within the time limit
    tunnels = [(extract_valves(tunnel), calc_pressure(tunnel, valves)) for tunnel in find_cave(
        path=[], node=root, time_remain=time_lim, 
        working_valves=working_valves - {root},                                              
        dists=dists)]
    logger.info(f'{len(tunnels)} paths found')
    logger.debug(f'first tunnel: {tunnels[0]}')
    logger.info('sorting paths by released pressure')
    tunnels = sorted(tunnels, key=lambda t: t[1], reverse=True)
    if part_two:
        # look for all disjoint sets
        pmax = 0
        for i, (human, ph) in enumerate(tunnels):
            if 2 * ph < pmax: 
                # stop searching once we've reached the lower release paths
                break
            for elephant, pe in tunnels[i+1:]:

                if ph + pe > pmax and set(human).isdisjoint(elephant):
                    pmax = max(pmax, ph + pe)
                    # hmax = human
                    # emax = elephant
                    # logger.debug(f'new max {human} and {elephant}')
                    logger.info(f'highest so far: {pmax}')
        # logger.info(f'highest release: {pmax}\nhuman: {hmax}\nelephant: {emax}')
        logger.info(f'highest release: {pmax}')

    else:
        # output
        # logger.debug(f'dists:\n{dists}')
        logger.info(f'max release: {max(tunnels, key=lambda t: t[1])}')
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
