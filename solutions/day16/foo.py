#!/usr/bin/env python

import argparse
import random

def find_tunnel():
    root = 'a'
    pool = 'bcd'
    path = [root]
    for cave in pool:
        yield find_next_cave(path + [cave], pool)

def find_next_cave(path, pool):
    print(f'current path: {path}')
    for cave in pool:
        if cave in path:
            continue
        else:
            print(f'adding {cave} to path')
            yield from find_next_cave(path + [cave], pool)
    # if all are in path, return
    yield cave

if __name__ == '__main__':
    tunnels = find_tunnel()
    for t in tunnels:
        print([c for c in t])

    print(tunnels)



