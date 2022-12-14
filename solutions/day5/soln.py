#! /usr/bin/env python
""" AoC 2022 Day 5 - Crates on stacks
"""
import sys
from collections import deque
import string

def load_input(fp: str):
    with open(fp, 'r') as f_in:
        for line in f_in.read().splitlines():
            yield line

def parse_schematics(schematic: list[str]) -> list[deque]:
    """Ingest the ascii schematic of stacks into list of deques
    Assumes the schematics denote crates by capital letter
    enclosed by [], and stack number by the last line in list
    In essence we're transposing the diagram
    """


def parse_procedure(procedure: str):
    """
    Translates "move 1 from 2 to 3" to args for stack methods:
    - move 1 from 2: deque2.pop()
    - to 3: deque3.append()

    Returns three ints 
    - number of crates to move
    - which stack to take
    - which stack to append
    """
    stack_args = [int(num) for num in procedure.split(sep=" ") if num in string.digits]
    return stack_args


def parse_input():
    """
    Read until blank line, at which point the rearrangement
    procedure starts
    """
    fn = sys.argv[1]
    fp = f"{fn}.txt"
    schematics = []
    input_file = load_input(fp)
    for line in input_file:
        if line != "":
           schematics.append(line)

        else:
            break
    procedure = [line for line in input_file]
    if fn == "test":
        print("--- schematics ---")
        for line in schematics:
            print(line)
        print("--- procedure ---")
        for line in procedure:
            stack_args = parse_procedure(line)
            print(f"move: {stack_args[0]}\tfrom: {stack_args[1]}\tto: {stack_args[2]}")
if __name__ == "__main__":
    parse_input()

