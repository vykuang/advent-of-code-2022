#! /usr/bin/env python
"""
AoC 2022 day 2 - rock paper scissors
"""
import sys


def load_input(fp: str):
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

def make_rps_dict(rock: int = 1, paper: int = 2, scissors: int = 3) -> dict:
    """Returns score dict based on player choice"""
    rps_dict = {
        "X": rock,
        "Y": paper,
        "Z": scissors,
    }
    return rps_dict

if __name__ == "__main__":
    try:
        fn = sys.argv[1] # test or input
        fp = f"{fn}.txt"
        rps_dict = make_rps_dict()
        score_dict = make_score_dict()
        scores = []
        for line in load_input(fp):
            match_scr = score_dict[line]
            rps_scr = rps_dict[line[-1]]
            total_scr = match_scr + rps_scr
            if fn == "test":
                print(f"line: {line}\tscore: {match_scr}")
                print(f"flat score: {rps_scr}")
                print(f"round total: {total_scr}")
            scores.append(total_scr)
        print(sum(scores))
    except IndexError as e:
        print(f"Error: only one arg, {input, test}, accepted")
