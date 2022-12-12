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

def make_decision_dict(scr_x: int = 1, scr_y: int = 2, scr_z: int = 3) -> dict:
    decision_dict = {
        "A X": scr_z, # lose (X) to A: play Z
        "A Y": scr_x, # tie to A: play X
        "A Z": scr_y, # win vs A: play Y
        "B X": scr_x,
        "B Y": scr_y,
        "B Z": scr_z,
        "C X": scr_y,
        "C Y": scr_z,
        "C Z": scr_x,
    }
    return decision_dict

def make_rps_dict(scr_x: int = 1, scr_y: int = 2, scr_z: int = 3) -> dict:
    """Returns score dict based on player choice"""
    rps_dict = {
        "X": scr_x,
        "Y": scr_y,
        "Z": scr_z,
    }
    return rps_dict

if __name__ == "__main__":
    try:
        fn = sys.argv[1] # test or input
        fp = f"{fn}.txt"
        rps_dict = make_rps_dict()
        score_dict = make_score_dict()
        scores = []
        rps_dict2 = make_rps_dict(scr_x=0, scr_y=3, scr_z=6)
        decision_dict = make_decision_dict()
        rps2 = []
        decision2 = []
        for line in load_input(fp):
            match_scr = score_dict[line]
            rps_scr = rps_dict[line[-1]]
            total_scr = match_scr + rps_scr
            if fn == "test":
                print(f"part A -----------------------")
                print(f"line: {line}\tscore: {match_scr}")
                print(f"flat score: {rps_scr}")
                print(f"round total: {total_scr}")
            rps2.append(rps_dict2[line[-1]]) # is it win, lose, or tie?
            decision2.append(decision_dict[line])
            scores.append(total_scr)
        print(sum(scores))
        print(f"Part II sum:\n{sum(rps2) + sum(decision2)}")
    except IndexError as e:
        print(f"Error: only one arg, {input, test}, accepted")
