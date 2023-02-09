#! /usr/bin/env python
"""
AoC 2022 Day
"""

import sys
import logging
from collections import defaultdict
from functools import reduce
import re
import time
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()


class Valve:
    def __init__(self, name='', rate=0, neighbors=None):
        """To use in defaultdict, must set defaults"""
        self.name = name
        self.rate = rate
        if neighbors:
            self.neighbors = set(neighbors)
        else:
            self.neighbors = None           
        
    def __repr__(self):
        return self.name

def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

def parse_valve_tunnel(line: str) -> list:
    """Parse input to return 
    - valve name: str
    - rate: int
    - neighbors: list[str]
    in the form of a Valve object
    """
    v = re.compile('[A-Z]{2}')
    r = re.compile('rate=(\d+)')
    v_m = v.findall(line)
    r_m = r.findall(line)
    return Valve(v_m[0], int(r_m[0]), v_m[1:])


def dijkstra_valves(graph: dict, source: str) -> dict:
    """
    Find shortest paths between all pairs of vertices.
    Assumes all neighboring nodes have distance=1
    
    Parameters
    ---------
    graph: dict
        dict of all nodes, with Node object as the value
    source: str
        name of source node
    
    Returns
    -------
    shortest_paths: dict
        keyed by nodes, the dict contains the shortest distance to each neighboring node
    """
    # mark all nodes really far, and mark all nodes unvisited
    dist = defaultdict(lambda: 1000) # {node1: dist1, node2: dist2, ...}
    unvisited = list(graph.keys())
    # prev = defaultdict(lambda: "")
        
    # print(f'unvisited:\n{unvisited}')
    # 2. assign distance=0 to origin
    dist[source] = 0
    
    while unvisited:
        # pop node with lowest dist
        current = sorted(unvisited, key=lambda x: dist[x])[0]
        unvisited.remove(current)
        
        # consider each neighbor
        for neighbor in graph[current].neighbors:
            if neighbor in unvisited:
                
                if dist[neighbor] > (new_dist := dist[current] + 1):
                    dist[neighbor] = new_dist
                    # prev[neighbor] = current
            
    return dist

def tunnel_dfs(graph: dict, current: str, path: defaultdict(int), time_remain: int = 30, time_lim: int = 30) -> list:
    """
    Search through all the possible paths in our volcano network
    
    Params
    ------
    graph: dict
        dict of all Valve nodes which contains release rate and neighbors
        
    source: str
        name of starting Valave node
        
    path: dict
        current path, {valve1: t_remain1, valve2: t_remain2, ...}. If a valve
        is in path, it has been visited in current path
        
    time_remain: int
        time remaining at current node
        
    time_lim: int
        time limit; accounts for 1 min valve opening and 1 min travelling
        between valve nodes
        
    Returns
    -------
    valve_paths: list
        contains dict {valve_id: time_release, ...} which represents each path
        and the order and timing in which the valves were opened
        e.g. if valve 'BB' was reached in minute 1, and opened by minute 2, the
        first entry would be {"BB": 28, ...}
    """
    # print(f'current: {current}\ttime_remain: {time_remain}')
    if not path:
        # print('path is empty; initialize time_remain')
        time_remain = time_lim
        
    # do path recording here
    path[current] = time_remain
    candidates = [node for node in tunnels 
                  if (node not in path.keys()) 
                  and (time_remain >= dists[current][node] + 2)]
    # print(f'neighbors:\n{candidates}')
    if candidates:
        for node in candidates:
            # yield from handles the fact that each tunnel_dfs call has a
            # for node in candidates: yield ...
            # t - dist - 1 accounts for valve opening
            yield from tunnel_dfs(graph, node, path.copy(), time_remain - dists[current][node] - 1, time_lim)
    else:
        # no more viable candidates; end of path reached
        # path_count += 1
        # print(f'\r{path_count} paths found', end='', flush=True)
        yield path
        
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

    t_a = time.time()
    SOURCE = 'AA'
    # parse puzzle input into valves
    tunnels = {valve.name: valve
                for line in load_input(fp)
                if (valve := parse_valve_tunnel(line))}
    
    # build dict of shortest paths from each point
    dists = {valve: dijkstra_valves(tunnels, valve) for valve in tunnels}
    
    paths = tunnel_dfs(
        graph=tunnels,
        current=SOURCE,
        path=defaultdict(int),
    )
    totals = {"->".join(p.keys()): reduce(
    lambda subtot, valve: subtot + p[valve] * tunnels[valve].rate, 
    p, 0) for p in paths}
    print(f"max pressure released: {max(totals.items(), key=lambda p: p[1])}")
    t_b = time.time()
    print(f"runtime: {t_b - t_a:3f} sec")
    
    