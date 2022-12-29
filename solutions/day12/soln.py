#! /usr/bin/env python
"""
AoC 2022 Day
"""

import sys
import logging

from collections import defaultdict

logger = logging.getLogger(__name__)

def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

class Graph:
    def __init__(self, nodes: str):
        self.adj_list = defaultdict(list)
        self.nodes = nodes
        self.visited = [False] * nodes
                
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
    for line in load_input(fp):
