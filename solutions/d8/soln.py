#! /usr/bin/env python
"""
AoC 2022 Day 8
Tree visibility
"""
import sys


def load_input(fp):
    with open(fp, "r") as f_in:
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
    visible = []
    idx = 0
    while len(visible) < len(treeline):
        horizon = treeline[idx:]
        current_max = max(horizon)
        # this max_idx is relative to idx
        num_invis = len(horizon) - 1 - horizon[::-1].index(current_max)
        # set all between idx and current_max_idx invis
        invis_bool = num_invis * [False]
        visible.extend(invis_bool)
        visible.append(True)  # for current_max
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


def make_views(row, col, grid, transposed):
    """Given the row and col position of the grid, return the
    views in the four cardinal direction towards the edges

    Returns
    left: list[str]
        node values starting from node towards the left
        ordering is such that the first value of the list is closest
        to the node, and the last value farthest
        In case of left, this means the ordering is reverse of the
        actual grid positioning
    right: list[str]
    top: list[str]
    bottom: list[str]
    """
    # print(f"row: {row}\tcol: {col}\tnode: {grid[row][col]}")
    left = grid[row][:col][::-1]
    right = grid[row][col + 1 :]
    top = transposed[col][:row][::-1]
    bottom = transposed[col][row + 1 :]

    return left, right, top, bottom


def find_scene(node: int, view: str) -> int:
    """Given the node height, and a str of digits representing the view of tree
    heights, find the pos of the nearest node of the same height, or higher
    Returns
    scene_score: int
        relative position of the first node is that equal or taller
        than the given node
    """
    #    print("new view")
    #    for height in view:
    #        print(f"{height}: {type(height)}")
    heights = set([int(height) for height in view])
    candidates = [str(height) for height in heights if height >= node]
    # look for pos of each node equal or taller

    if candidates:
        ht_pos = [view.index(height) for height in candidates]
        # take the minimum
        if ht_pos:
            scene_score = min(ht_pos) + 1
        else:
            scene_score = 1
    else:
        scene_score = len(view)
    # print(f"view score: {scene_score}")
    return scene_score


if __name__ == "__main__":
    fn = sys.argv[1]
    test = fn == "test"
    fp = f"{fn}.txt"
    grid = [line for line in load_input(fp)]
    vis_grid_right = [find_visible(line) for line in grid]
    vis_grid_left = [find_visible(line, from_left_or_bottom=True) for line in grid]

    grid_transpose = transpose_grid(grid)
    vis_grid_top = [find_visible(line) for line in grid_transpose]
    vis_grid_bot = [
        find_visible(line, from_left_or_bottom=True) for line in grid_transpose
    ]
    # transpose the top/bot vis grid back to original shape
    # to take logical AND with the left/right vis grid
    vis_grid_top = transpose_grid(vis_grid_top)
    vis_grid_bot = transpose_grid(vis_grid_bot)
    # take the OR of all four matrices;
    # visibility from any one direction counts
    vis_grid = [
        [
            any([r, l, t, b])
            for r, l, t, b in zip(
                vis_grid_right[row],
                vis_grid_left[row],
                vis_grid_top[row],
                vis_grid_bot[row],
            )
        ]
        for row in range(len(vis_grid_right))
    ]
    vis_sum = sum([sum(row) for row in vis_grid])
    print(f"total visible: {vis_sum}")

    # part ii
    max_scene = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            node = int(grid[row][col])
            views = make_views(row, col, grid, grid_transpose)
            scenes = [find_scene(node, view) for view in views]
            scene_score = 1
            for scene in scenes:
                scene_score *= scene

            if scene_score > max_scene:
                max_scene = scene_score

            if test:
                print(f"[{row}, {col}]: {scene_score}")
    print(f"Max scene score: {max_scene}")
