#!/usr/bin/env python3
from pathlib import Path
import argparse
import logging
import sys
from time import time_ns
from operator import attrgetter
import re

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def read_line(fpath: str):
    """Reads the input and yields each line"""
    path = Path(fpath)
    with open(fpath) as f:
        yield from f

def traverse(board, pos, face, nmov, wall='#', path='.') -> complex:
    """
    Traverses the board using the puzzle's wrap-around logic
    and returns the arrival pos
    """
    logger.debug(f'from {pos}, {nmov} towards {face}')
    moved = 0
    while moved < nmov:
        chk = pos + face
        # check for wall or wraparound
        if not (tile := board.get(chk)):
            # wrap
            logger.debug(f'wrap from {pos}')
            match face:
                case -1:
                    chk = max([tile for tile in board.keys()
                        if tile.imag == pos.imag],
                        key=attrgetter('real'))
                case -1j:
                    chk = max([tile for tile in board.keys()
                        if tile.real == pos.real],
                        key=attrgetter('imag'))
                case 1:
                    chk = min([tile for tile in board.keys()
                        if tile.imag == pos.imag],
                        key=attrgetter('real'))
                case 1j:
                    chk = min([tile for tile in board.keys()
                        if tile.real == pos.real],
                        key=attrgetter('imag'))
        if (tile := board.get(chk)) == wall:
            logger.debug('wall; break')
            break 
        if tile == path:
            moved += 1
            pos = chk
            continue
    return pos


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
    # maze diagram first, then blank line, then path
    lines = read_line(fp)
    line = next(lines)
    row = 1
    board = {}
    while line.strip():
        logger.debug(f'row {row}: {line}')
        new_pos = {col + 1 + row * 1j: ch
                for col, ch in enumerate(line)
                if ch in ['.', '#']}
        board.update(new_pos)
        row += 1
        line = next(lines)
    path = next(lines).strip() # num - RL - num - ... - RL - num
    logger.debug(f'{path}')
    # execute
    start = min([pos for pos, tile in board.items() if tile == '.'],
            key=attrgetter('imag', 'real'))
    logger.debug(f'start: {start}')
    tstart = time_ns()

    # run the initial segment
    pos_face = 1 # right
    hit = re.match(r'\d+', path)
    nmov = int(hit.group(0))
    pos_curr = traverse(board, start, pos_face, nmov)
    path = path[hit.end():]
    while path.strip():
        # consume while we traverse
        logger.debug(f'path remaining: {path}')
        turn = path[0]
        if turn == 'R':
            pos_face *= 1j
        else:
            pos_face *= -1j
        path = path[1:]
        hit = re.match(r'\d+', path)
        nmov = int(hit.group(0))
        pos_curr = traverse(board, pos_curr, pos_face, nmov)
        path = path[hit.end():]
        
    vface = dict(zip([1,1j,-1,-1j], range(4)))
    pw = 1000 * pos_curr.imag + 4 * pos_curr.real + vface[pos_face]
    # output
    logger.info(f'pw: {pw}')

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
