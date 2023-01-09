#! /usr/bin/env python
"""
AoC Day 3 - rucksack reorganization
"""
from pathlib import Path
import sys
from string import ascii_lowercase, ascii_uppercase


def make_priority_dict() -> dict:
    """Create dict mapping lower case to 1-26 and upper case to 27-52"""
    priority_dict = {
        letter: priority + 1
        for priority, letter in enumerate(ascii_lowercase + ascii_uppercase)
    }
    return priority_dict


def load_input(fp: Path):
    """Loads the input file for compute"""
    with open(fp, "r") as f:
        for line in f.read().splitlines():
            yield line


def parse_rucksack(line: str):
    """Divides rucksack into two halves, one for each compartment

    Returns compart_a, compart_b for each compartment
    """
    compart_size = int(len(line) / 2)
    compart_a = line[:compart_size]
    compart_b = line[compart_size:]
    return compart_a, compart_b


def check_item(comp_a: str, comp_b: str) -> set:
    """Do any characters in comp_a match any in comp_b?
    If none in 'a' match any in 'b', the same is true vice versa, and so
    only one-way check is needed

    Returns the shared letter if so, otherwise returns None
    """
    set_a = set(comp_a)
    set_b = set(comp_b)
    # shared = [item for item in comp_a if item in set_b]
    shared = set_a.intersection(set_b)
    return shared


def check_badge(group: list) -> int:
    """Checks for the single common item between all rucksacks
    and return the mapped value
    """
    a, b, c = group
    shared_ab = check_item(a, b)
    shared = {item for item in c if item in shared_ab}
    return shared


if __name__ == "__main__":
    priority = make_priority_dict()
    priority_sums = []
    group_lim = 3
    group = []
    badge_list = []
    try:
        fn = sys.argv[1]
        fp = f"{fn}.txt"
        for line in load_input(fp):
            # part A - check common item between compartments in a rucksack
            comp_a, comp_b = parse_rucksack(line)
            # print(f"A: {comp_a}\tB:{comp_b}")
            shared = check_item(comp_a, comp_b)
            if shared:
                shared = shared.pop()
                # print(f"shared:\t{shared}\tpriority:\t{priority[shared]}")
                priority_sums.append(priority[shared])

            # part B - check common item between every three rucksacks
            group.append(line)
            if len(group) >= group_lim:
                group_badge = check_badge(group).pop()
                group_badge_priority = priority[group_badge]
                badge_list.append(group_badge_priority)
                group.clear()

    except:
        raise Exception
    print(f"Part A: priority sums: {sum(priority_sums)}")
    print(f"Part B: badge sums: {sum(badge_list)}")
