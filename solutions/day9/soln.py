#! /usr/bin/env python
"""
AoC 2022 Day 9 - Heads and Tails
"""

import sys

class Movement:
    way: str
    dist: str 

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
            history = [(point[0], point[1] + i + 1) for i in range(int(dist))] 
        case ["D", dist]:
            history = [(point[0], point[1] - i - 1) for i in range(int(dist))]
        case ["L", dist]:
            history = [(point[0] - i - 1, point[1]) for i in range(int(dist))]
        case ["R", dist]:
            history = [(point[0] + i + 1, point[1]) for i in range(int(dist))]
        case _:
            history = []
    return history

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
        head_hist = move_head(head, line)
        head = head_hist[-1]
        if test:
            print(f"line: {line}")
            print(f"head pos: {head}")
            print(f"head history: {head_hist}")
        
