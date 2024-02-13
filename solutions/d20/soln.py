#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    fpath = Path(fpath)
    with open(fpath) as f:
        yield from f

class Cnode:
    """Nodes in a circular doubly linked list"""
    def __init__(self, val) -> None:
        self.val = val
        self.prev = None
        self.next = None
    def __repr__(self) -> str:
        return f'val: {self.val}'
    

def create_circ_list(lines, decrypt=1):
    head = Cnode(decrypt*int(next(lines)))
    prev = head
    curr = Cnode(decrypt*int(next(lines)))
    prev.next = curr
    curr.prev = prev
    leng = 2
    for line in lines:
        # assign new nodes
        new_node = Cnode(decrypt*int(line))
        curr.next = new_node
        new_node.prev = curr
        # update
        prev = curr
        curr = new_node
        leng += 1

    # full circle
    curr.next = head
    head.prev = curr
    return head, leng

def print_circ(head, leng):
    idx = 1
    curr = head
    arr = [head.val]
    while idx < leng:
        curr = curr.next
        arr.append(curr.val)
        idx += 1

    return arr

def main(sample: bool, part_two: bool, loglevel: str):
    """ """
    logger.setLevel(loglevel)
    if not sample:
        fp = "input.txt"
    else:
        fp = "sample.txt"
    logger.debug(f"loglevel: {loglevel}")
    logger.info(f'Using {fp} for {"part 2" if part_two else "part 1"}')

    # read input
    decrypt = 811589153 if part_two else 1
    loops = 10 if part_two else 1
    head, leng = create_circ_list(read_line(fp), decrypt=decrypt)
    idx = 0
    curr = head
    order = []
    while idx < leng:
        # logger.debug(f'node {curr}\tprev {curr.prev}\tnext {curr.next}')
        order.append(curr)
        curr = curr.next
        idx += 1
    logger.info(f'len: {leng}')
    # execute
    tstart = time_ns()
    
    logger.debug(f'initial: {print_circ(head, leng)}')
    for _ in range(loops):
        for node in order:
            logger.debug(f'moving {node.val}')
            # bridging the gap
            node.prev.next = node.next
            node.next.prev = node.prev
            # prepping the move
            prv = node.prev
            nxt = node.next
            # movement
            for _ in range(node.val % (leng - 1)):
                prv = prv.next
                nxt = nxt.next
            # insertion
            node.prev = prv
            node.next = nxt
            # amend the insertion
            prv.next = node
            nxt.prev = node

    # starting from node.val = 0
    groves = 0
    curr = head
    while curr.val != 0:
        curr = curr.next
    for _ in range(3):
        for _ in range(1000):
            curr = curr.next

        groves += curr.val
    # output
    logger.info(f'sum: {groves}')
    tstop = time_ns()
    logger.info(f"runtime: {(tstop-tstart)/1e6} ms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    opt = parser.add_argument
    opt("--sample", "-s", action="store_true", default=False)
    opt("--part_two", "-t", action="store_true", default=False)
    opt("--loglevel", "-l", type=str.upper, default="info")
    args = parser.parse_args()
    main(args.sample, args.part_two, args.loglevel)
