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

def find_visible(line: str, from_left_or_bottom: bool = False):
    """
    Successively finds the new maximum to determine
    tree visibility.
    Makes use of list.index() behaviour that returns
    idx of the *first* occurrence

    If line is in original order, result indicates visibility from right. If reversed, visibility from left

    Returns a boolean array indicating visibility
    """
    if from_left_or_bottom:
        line = line[::-1]
    treeline = [int(height) for height in line]
    prev_max = treeline[0]
    current_max = max(treeline)
    visible = []
    idx = 0
    while len(visible) < len(treeline):        
        horizon = treeline[idx:]
        current_max = max(horizon)
        # this max_idx is relative to idx
        num_invis = len(horizon) - 1 - horizon[::-1].index(current_max)
        # set all between idx and current_max_idx invis
        invis_bool = [False for _ in range(num_invis)]
        visible.extend(invis_bool)
        visible.append(True) # for current_max
        # so it doesn't look for the same max()
        idx += num_invis + 1

    if from_left_or_bottom:
        visible.reverse()
    return visible

def transpose_grid(grid: list[list]) -> list[list]:
    """
    Takes a list of list (2D matrix) and transposes it

    Returns
    List of list: transposed grid
    """
    # width = len(grid[0])

    # transposed = [[row[col_pos] for row in grid] for col_pos in range(width)]
    # equivalent to
    transposed = list(zip(*grid))
    return transposed

if __name__ == "__main__":
    fn = sys.argv[1]
    test = fn == "test"
    fp = f"{fn}.txt"
    grid = [line for line in load_input(fp)]
    vis_grid_right = [find_visible(line) for line in grid]
    vis_grid_left = [find_visible(line, from_left_or_bottom=True) for line in grid]
    grid_transpose = transpose_grid(grid)
    vis_grid_top = [find_visible(line) for line in grid_transpose]

    vis_grid_bot = [find_visible(line, from_left_or_bottom=True) for line in grid_transpose]
    # transpose the top/bot vis grid back to original shape
    # to take logical AND with the left/right vis grid
    vis_grid_top = transpose_grid(vis_grid_top)
    vis_grid_bot = transpose_grid(vis_grid_bot)
    vis_grid = [[any([r,l,t,b]) for r,l,t,b in
        zip(vis_grid_right[row], vis_grid_left[row], vis_grid_top[row], vis_grid_bot[row])] for row in range(len(vis_grid_right))]
    vis_sum = sum([sum(row) for row in vis_grid])
    print(f"total visible: {vis_sum}")

