#! /usr/bin/env python
"""
AoC 2022 Day 15 - Sensors and beacons
"""

import sys
import logging
import re

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()

def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

def make_cmplx(line: str, pattern: re.compile) -> tuple:
    """Parse the input line into pair of complex numbers
    representing the sensor and beacon coordinates
    """
    sx, sy, bx, by = list(map(int, pattern.findall(line)))
    return complex(sx, sy), complex(bx, by)

def calc_man_dist(s: complex, b: complex) -> int:
    """Returns manhattan distance given two complex numbers
    that represent their cartesian coordinates
    """
    return int(abs((b-s).real)+abs((b-s).imag))

def calc_reach(s: complex, reach: int, row: int):
    logger.debug(f"sensor: {s}\treach: {reach}\trow:{row}")
    r_new = reach - abs(row - s.imag)
    logger.debug(f"r_new: {r_new}")
    if r_new > 0:
        left = (s.real - r_new)
        logger.debug(f"reach > 0; left edge on target row: {left}")
        return [left, r_new*2]
    else:
        return None

def beacon_elim(target: int, reach: list, sb_pairs: list = None):
    """
    Given a sorted list of left edges and their reach, find
    how many nodes cannot contain a beacon
    
    Parameters
    --------
    target: int
        Beacon elimination will be conducted for this row
    reach: list(tuple)
        each tuple contains the left edge and the reach of the sensor detection
        cone
    sb_pairs: list
        list of tuples containing location of sensors and beacons
        in complex coordinates
    
    Returns
    -------
    num_empty: int
        number of nodes on the target row that cannot contain beacon
    """
    # sort by left edge
    reach_sorted = sorted(reach, key=lambda x: x[0])
    b_search = [int(b.real) for _, b in sb_pairs if b.imag == target]
    logger.debug(f"b_search list: {b_search}")
    b_search = set(b_search)
    logger.debug(f"b_search unique: {b_search}")
    s_search = [int(s.real) for s, _ in sb_pairs if s.imag == target]
    logger.debug(f"sensors on this row: {s_search}")
    search = set(s_search) | b_search
    logger.debug(f"search set: {search}")
    
    beacon = None
    ### incorporate into the loop
    left_prev, reach_prev = reach_sorted[0]
    right_prev = left_prev + reach_prev
    totals = []
    # logger.debug(f"left: {left_prev}, reach: {reach_prev}, right: {right_edge}")
    #############################
    
    # totals = [0]
    # left_prev = None
    for (left_edge, reach_new) in reach_sorted:
        logger.info(f"prev\tleft: {left_prev}\tright: {right_prev}")
        logger.info(f"curr\tleft: {left_edge}\tright: {left_edge+reach_new}\treach: {reach_new}")
                
        if (left_edge <= right_prev + 1) and totals:
            if ((right_edge := left_edge + reach_new) > right_prev):
                logger.debug(f"overlap - right_prev: {right_prev}\tright_new: {right_edge}")
                # update last subtotal accounting for overlap
                # if left_prev:
                totals[-1] += right_edge - right_prev
                # else:
                #     totals[-1] = right_edge - left_edge
                # update right edge only if it extends the edge
                right_prev = right_edge
            
        elif (left_edge > right_prev + 1) or not totals:
            # new segment
            totals.append(reach_new + 1)
            # update the edges
            left_prev = left_edge
            right_prev = right_edge = left_prev + reach_new
            logger.debug(f"new segment: {reach_new} added\nleft_prev: {left_prev}\tright_edge: {right_edge}")
            if left_edge > 0:
                beacon = complex(left_edge - 1, target)
            
        else:
            pass
        
        # check for beacons
        for d in search.copy():
            logger.debug(f"considering node {d}")
            if left_edge <= d and d <= right_edge:
                totals[-1] -= 1
                search.discard(d)
                logger.debug(f"device found within range at node {d}")
                logger.debug(f"subtotal corrected to {totals[-1]}")
        
        logger.debug(f"totals: {totals}")
    return sum(totals), beacon
    
def find_tuning(min_xy, max_xy, dists, sb_pairs):
    """
    Find the beacon location, given the min and max possible coordinates
    """
    for row in range(min_xy, max_xy + 1):
        logger.info(f"row: {row}")
        print(f"\rrow: {row}", end="", flush=True)
        reaches = [d for xy, reach in zip(sb_pairs, dists) if (d := calc_reach(xy[0], reach, row))]
        # enforce the coordinate limit in reaches
        for i, (edge, reach) in enumerate(reaches):
            if edge < min_xy:
                logger.info(f"{edge} < {min_xy}: replace.")
                reaches[i][0] = min_xy
            if (right_lim := edge + reach) > max_xy:
                reaches[i][1] = max_xy - right_lim
                logger.info(f"{right_lim} > {max_xy}. new reach: {reaches[i][1]}")
        num_empty, beacon = beacon_elim(row, reaches, sb_pairs)
        if beacon:
            return beacon, int(beacon.real * 4000000 + beacon.imag)
        
if __name__ == "__main__":
    fn = sys.argv[1]
    match fn:
        case "test" | "input":
            fp = f"{fn}.txt"
            test = fn == "test"
        case _:
            raise ValueError(f"{fn} cannot be used")
    p1 = False
    if test and p1:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.WARNING
    logger.setLevel(loglevel)
    ch.setLevel(loglevel)
    logger.addHandler(ch)

    # optional '-', one or more numbers
    pattern = re.compile('-?\d+')
    sb_pairs = [make_cmplx(line, pattern) for line in load_input(fp)]
        
    logger.debug(f"test coordinates:\n{sb_pairs}")
    dists = [calc_man_dist(s, b) for s, b in sb_pairs]
    logger.debug(f"manhattan distances:\n{dists}")
    if p1:
        reaches = [d for xy, reach in zip(sb_pairs, dists) if (d := calc_reach(xy[0], reach, row))]
        logger.debug(f"(left, reach):\n{reaches}")
        num_empty, beacon = beacon_elim(row, reaches, sb_pairs)
        print(f"empty nodes: {num_empty}\tbeacon xy: {beacon}")
    
    # part two
    min_xy = 0
    if test:
        max_xy = 20
    else:
        max_xy = 4000000
    beacon, freq = find_tuning(min_xy, max_xy, dists, sb_pairs)
    print(f"beacon loc: {beacon}\nfreq: {freq}")

    
