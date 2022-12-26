#! /usr/bin/env python
"""
AoC 2022 Day 9 - Heads and Tails
"""
import math
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

def move_tail(tail: tuple, head_hist: list):
    """
    Given a snippet of head's position history,
    determine if tail needs to be moved to maintain adjacency, and move
    accordingly
    Assumes the first coordinates in head_hist is the next coordinate in the
    path, and that tail may not be adjacent to that coordinate

    Returns
    tail_hist: list[tuple]
        history of the tail positions based on head_hist
    """
    tail_hist = []
    for head in head_hist:
    # same row/col?
        if tail == head:
            continue

        if find_dist(head, tail) >= 2.0: 
            # move tail and update list
            x_diff = head[0] - tail[0]
            y_diff = head[1] - tail[1]
            if x_diff:
                x_move = x_diff / math.fabs(x_diff)
            else:
                x_move = 0
            if y_diff:
                y_move = y_diff / math.fabs(y_diff)
            else:
                y_move = 0

            tail = (tail[0] + x_move, tail[1] + y_move)
            tail_hist.append(tail)
    return tail_hist

def find_dist(a, b) -> float:
    """Returns cartesian distance between a and b
    a, b: tuple(x, y)
    """
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

                
    
if __name__ == "__main__":
    fn = sys.argv[1]
    match fn:
        case "test" | "input":
            fp = f"{fn}.txt"
            test = fn == "test" 
        case _:
            raise ValueError(f"{fn} cannot be used")
            
    # initialize position at origin
    head = (0, 0)
    tail = head
    tail_hist = []
    tail_hist.append(tail)
    for line in load_input(fp):
        head_hist = move_head(head, line)
        tail_hist.extend(move_tail(tail, head_hist))
        head = head_hist[-1]
        if tail_hist:
            tail = tail_hist[-1]
        if test:
            print(f"line: {line}")
            print(f"head pos: {head}")
            print(f"head history: {head_hist}")
            print(f"tail pos: {tail}")
            print(f"tail history: {tail_hist}")
    tail_pos_unique = set(tail_hist)
    print(f"tail has been to {len(tail_pos_unique)} points")
