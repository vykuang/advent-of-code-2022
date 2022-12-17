#! /usr/bin/env python
"""
AoC 2022 Day 8
Tree visibility
"""
import sys

def load_input(fp):
    with open(fp, 'r') as f_in:
        for line in f_in.read().splitlines():
            yield line

def find_visible(line: str):
    """
    Successively finds the new maximum to determine
    tree visibility.
    Makes use of list.index() behaviour that returns
    idx of the *first* occurrence

    If line is in original order, result indicates visibility from right. If reversed, visibility from left

    Returns a boolean array indicating visibility
    """
    treeline = [int(height) for height in line]
    prev_max = treeline[0]
    current_max = max(treeline)
    visible = []
    idx = 0
    while len(visible) < len(treeline):        
        # print(f"current idx: {idx}")
        horizon = treeline[idx:]
        current_max = max(horizon)
        # this max_idx is relative to idx
        num_invis = len(horizon) - 1 - horizon[::-1].index(current_max)
        # set all between idx and current_max_idx invis
        invis_bool = [False for _ in range(num_invis)]
        visible.extend(invis_bool)
        visible.append(True) # for current_max
        # so it doesn't look for the same max()
        idx = num_invis + 1

    return visible

if __name__ == "__main__":
    fn = sys.argv[1]
    fp = f"{fn}.txt"
    for line in load_input(fp):
        vis_right = find_visible(line)
        vis_left = list(reversed(find_visible(reversed(line))))
        if fn == "test":
            print(line)
            print(f"Vis from right:\t{vis_right}")
            print(f"Vis from left:\t{vis_left}")

