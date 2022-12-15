#! /usr/bin/env python
"""
AoC 2022 Day 6 - signal processing
Identify the first sequence of unique letters
"""
import sys

def load_input(fp: str):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

def parse_test_input(line: str):
    """
    Test input file has multiple lines,
    test input first, followed by the answer separated by ' '

    Returns
    str and test solution
    """
    data, pos = line.split(sep=" ")
    return data, int(pos)

def find_unique_seq(data: str, seq_len: int = 4):
    """
    Given a stream of characters, find the first sequence that comprises
    entirely of uniques that are seq_len long
    """

