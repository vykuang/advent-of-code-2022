from pathlib import Path
import sys

def load_input(fp: Path):
    """Loads the input file for compute"""
    with open(fp, "r") as f:
        for line in f.read().splitlines():
            yield line 
def sum_calorie(group: list):
    """Sum numbers in a list"""
    total = 0
    for calorie in group:
        total += calorie
    return total

def parse_elf_calories(calories_fp: str, top_n: int = 3):
    """Parse the inventory into list of arrays"""
    group = []
    sums = []
    for line in load_input(calories_fp):
        if line != "":
            group.append(int(line))
        else:
            # move on to next group
            sums.append(sum_calorie(group))
            group = []
    sums.append(sum_calorie(group))
    sums = sorted(sums, reverse=True)
    return sums[:top_n]
    

if __name__ == "__main__":
    try:
        if sys.argv[1] == "test":   
            sums = parse_elf_calories("test.txt")
            print(sums)
            print(max(sums))
        elif sys.argv[1] == "input":
            sums = parse_elf_calories("input.txt")
            print(max(sums))
            print(sum_calorie(sums))
    except IndexError as e:
        print("No arg received:", e)
