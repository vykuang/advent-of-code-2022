#! /usr/bin/env python
"""
AoC 2022 Day 6 - signal processing
Identify the first sequence of unique letters
"""
import sys
from collections import deque


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
    data, packet_pos, msg_pos = line.split(sep=" ")
    return data, int(packet_pos), int(msg_pos)


def find_unique_seq(data: str, seq_len: int = 4):
    """
    Given a stream of characters, find the first sequence that comprises
    entirely of uniques that are seq_len long

    Keep a rolling deque that is seq_len long, popleft the oldest and append
    the new char, and use to check if the next char is in this window
    """
    window = deque()
    # initialize our window
    for i in range(seq_len):
        window.append(data[i])

    for i, char in enumerate(data[seq_len:]):
        if len(set(window)) < len(window):
            window.popleft()
            window.append(char)
        else:
            print(f"marker found: {window}\nend pos: {i+seq_len}")
            break
    return i + seq_len


if __name__ == "__main__":
    fn = sys.argv[1]  # test or input
    fp = f"{fn}.txt"
    if fn == "test":
        lines = load_input(fp)
        test_inputs = [parse_test_input(line) for line in lines]
        test_pos = [find_unique_seq(test_input[0]) for test_input in test_inputs]
        print(f"test_pos:\n{test_pos}")
        print(f"answer:\n{[test_input[1] for test_input in test_inputs]}")

        test_msg_pos = [
            (find_unique_seq(test_input[0], 14), test_input[2])
            for test_input in test_inputs
        ]
        print(f"test_msg_pos:\n{test_msg_pos}")
    elif fn == "input":
        lines = load_input(fp)
        for line in lines:
            mark_pos = find_unique_seq(line)
            msg_pos = find_unique_seq(line, 14)
            print(len(line))
