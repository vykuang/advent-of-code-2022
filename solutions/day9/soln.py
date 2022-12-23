#! /usr/bin/env python
"""
AoC 2022 Day 9 - Heads and Tails
"""

import sys

def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

def move_head(point: tuple, line: str):
    """Given a heading and distance, move the head and collect
    the nodes which the head travels through

    Returns
    head_places: list
        list of coordinates where the head has been as a result of
        the direction
    """
    match line.split(" "):
        case ["U", dist]:
            history = [(point[0], point[1]+1) for _ in dist]
if __name__ == "__main__":
    fn = sys.argv[1]
    match fn:
        case "test" | "input":
            fp = f"{fn}.txt"
            test = fn == "test" 
        case _:
            raise ValueError(f"{fn} cannot be used")
            
    head = [0, 0]
    tail = head
    for line in load_input(fp):
        head = move_head(line)
