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

def make_schem_dict(schematic: list[str]) -> dict:
    """Ingest the ascii schematic of stacks into list of deques
    Assumes the schematics denote crates by capital letter
    enclosed by [], and stack number by the last line in list
    In essence we're transposing the diagram
    """
    stack_ids = [stack_id for stack_id in schematic[-1].split(sep=" ")
        if stack_id and stack_id in string.digits]
    stack_pos = [list(schematic[-1]).index(stack_id) for stack_id in stack_ids]
    return dict(zip(stack_pos, stack_ids))

def make_stacks(schematic: list[str]):
    """Build the stacks based on parsed schematic"""
    # make schem_dict
    schem_dict = make_schem_dict(schematic)
    # initialize stacks
    stacks = [deque() for _ in schem_dict]
    # start from bottom
    for line in schematic[-2::-1]:
        crates = [crate for crate in line if crate in string.ascii_letters]
        for crate in crates:
            stack_pos = line.index(crate)
            stack_id = int(schem_dict[stack_pos]) - 1 # zero-index in list
            stacks[stack_id].append(crate)

    return stacks            
        
def parse_procedure(procedure: str):
    """
    Translates "move 1 from 2 to 3" to args for stack methods:
    - move 1 from 2: deque2.pop()
    - to 3: deque3.append()

    Need to also parse double-digits as one number

    Returns three ints 
    - number of crates to move
    - which stack to take
    - which stack to append
    """
    stack_args = [int(num) for num in procedure.split(sep=" ") if num in string.digits]
    stack_args[1] -= 1
    try:
        stack_args[2] -= 1 # to account for zero-based index
    except IndexError as e:
        print(e)
        print(procedure)
    return stack_args

def move_crates():
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
    stacks = make_stacks(schematics)
    procedure = [line for line in input_file]
    for i, line in enumerate(procedure):
        if line:
            stack_args = parse_procedure(line) # move x from y to z
            moved = deque()
            for _ in range(stack_args[0]):
                try:
                    moved.append(stacks[stack_args[1]].pop())
                except IndexError as e:
                    print(f"Line {i}: {procedure[i]}", e)
            stacks[stack_args[2]].extend(moved)
        else:
            break
    top_crates = [stacks[i].pop() for i in range(len(stacks))]
    
    if fn == "test":
        print("--- schematics ---")
        for line in schematics:
            print(line)

        print(make_schem_dict(schematics))
        for i, stack in enumerate(stacks):
            print(f"stack {i+1}:\n{stack}")
        print("--- procedure ---")
        for line in procedure:
            stack_args = parse_procedure(line)
            print(f"move: {stack_args[0]}\tfrom: {stack_args[1]}\tto: {stack_args[2]}")

    return top_crates

if __name__ == "__main__":
    top_crates = move_crates()
    print(f"Top crates: {top_crates}")
