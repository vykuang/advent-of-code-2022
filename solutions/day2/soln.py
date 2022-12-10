#! /usr/bin/env python
"""
AoC 2022 day 2 - rock paper scissors
"""
import sys


def load_input(fp: Path):
    """Loads the input file for compute"""
    with open(fp, "r") as f:
        for line in f.read().splitlines():
            yield line 

def make_score_dict(lose: int = 0, tie: int = 3, win: int = 6) -> dict:
    """Returns score dict based on puzzle rules"""
    score_dict = {
        "A X": tie,
        "A Y": win,
        "A Z": lose,
        "B X": lose,
        "B Y": tie,
        "B Z": win,
        "C X": win,
        "C Y": lose,
        "C Z": tie,
    }
    return score_dict
