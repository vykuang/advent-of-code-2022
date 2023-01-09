#! /usr/bin/env python
"""
AoC 2022 Day 9 - Heads and Tails
"""
import math
import sys
import logging

logger = logging.getLogger(__name__)


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
    tail_hist = [tail]
    logger.debug(" - - - - - - ")
    logger.debug(f"initial pos: {tail_hist}")
    for head in head_hist:
        # same row/col?
        logger.debug(f"tail @ {tail}\thead @ {head}")
        if tail == head:
            continue

        if find_dist(head, tail) >= 2.0:
            # move tail and update list
            logger.debug("move tail")
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
            logger.debug(f"new tail @ {tail}")
            tail_hist.append(tail)
            logger.debug(f"tail path: {tail_hist}")
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
        case "test" | "input" | "test2":
            fp = f"{fn}.txt"
            test = "test" in fn
        case _:
            raise ValueError(f"{fn} cannot be used")
    if test:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
    else:
        logger.setLevel(logging.INFO)
    LEN_ROPE = 10
    # initialize position at origin
    head = (0, 0)
    # initialize positions of knots
    rope = [head for _ in range(LEN_ROPE)]
    # init collections of knot positions as list of sets
    rope_hists = [[head] for _ in range(LEN_ROPE)]
    for line in load_input(fp):
        logger.debug("====================")
        logger.debug(f"line: {line}")
        for i, [tail_hist, tail] in enumerate(zip(rope_hists, rope)):
            logger.debug(f"knot {i} @ {tail}")
            if i < 1:  # skip the head in the beginning
                path = move_head(tail, line)
            else:
                path = move_tail(tail, prev_path)
            # I don't think enum/zip returns the same thing
            # tail = path[-1]
            # tail_hist.extend(path)
            rope[i] = path[-1]
            rope_hists[i].extend(path)
            prev_path = path
            logger.debug(f"path: {path}")
            logger.debug(f"knot {i} now @ {rope[i]}")
            logger.debug("----------------------")
    end_knot_pos = set(rope_hists[-1])
    print(f"tail has been to {len(end_knot_pos)} points")
