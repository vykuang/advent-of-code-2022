from pathlib import Path

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

def parse_elf_calories(calories_fp: str):
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

    return sums

if __name__ == "__main__":
   sums = parse_elf_calories("test.txt")
   print(sums)
   print(max(sums))
