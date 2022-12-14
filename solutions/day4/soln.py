#! /usr/bin/env python
"""
AoC 2022 Day 4
Camp cleanup
"""
import sys

def load_input(fp: str):
    """
    Generates line-by-line the input file
    """
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line 

def parse_sections(line: str, pair_delim: str = ',', section_delim: str = '-') -> tuple:
    """
    Parse the line into two sections, given the delimiter, and then
    into the section IDs
    """
    sec_a, sec_b = line.split(sep=pair_delim)
    a_lb, a_ub = [int(bound) for bound in sec_a.split(sep=section_delim)]
    b_lb, b_ub = [int(bound) for bound in sec_b.split(sep=section_delim)]
    return a_lb, a_ub, b_lb, b_ub

def check_subset(a_lb, a_ub, b_lb, b_ub) -> bool:
    """Does all of A fit into B, or vice versa?
    """
    if a_lb >= b_lb and a_ub <= b_ub:
        return True
    elif b_lb >= a_lb and b_ub <= a_ub:
        return True

    else:
        return False

def check_overlap(a_lb, a_ub, b_lb, b_ub) -> bool:
    """Checks for any overlap between a and b
    Scenarios to check:
    1. both a_ub and a_lb < b_lb
    2. vice versa: both b_lb and b_ub < a_lb
    """
    if (a_lb < b_lb and a_ub < b_lb) or (b_lb < a_lb and b_ub < a_lb):
        return False 
    else:
        return True

if __name__ == "__main__":
    fp = f"{sys.argv[1]}.txt"
    subset_count = 0
    overlap_count = 0
    for line in load_input(fp):
        bounds = parse_sections(line)
        if check_subset(*bounds):
            subset_count += 1
            overlap_count += 1
        elif check_overlap(*bounds):
            overlap_count += 1
        else:
            pass
        if "test" in fp:
            print(line)
            print(parse_sections(line))
            print(f"Subset found: {check_subset(*parse_sections(line))}")
            print(f"overlaps found: {check_overlap(*bounds)}")

    print(f"total subset found: {subset_count}")
    print(f"total overlaps found: {overlap_count}")
