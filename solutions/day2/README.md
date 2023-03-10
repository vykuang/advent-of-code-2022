# Day 2 - Rock paper scissors

[Official puzzle link](https://adventofcode.com/2022/day/2)

- `A` - rock
- `B` - paper
- `C` - scissors

According a friendly elf, we are led to believe that we should play 

- `X` for rock,
- `Y` for paper
- `Z` for scissors

however that strategy is not confirmed, and could shift. Moreover the score for each round depends on what was played:

- 1 - rock
- 2 - paper
- 3 - scissors

Winning gives another set of scores:

- 0 - lose
- 3 - draw
- 6 - win

Compound with the fact that you don't actually want to win everytime to not raise suspicion, a strategy emerges:

- `A Y` - opp plays rock (A), and we should play paper (Y) to score 2 (for playing paper) + 6 (for winning) = 8 pts
- `B X` - opp: paper (B), we play rock (X) to gain 1 (for rock) + 0 (for losing) = 0 pts
- `C Z` - opp: scissors (C), we play scissors as well (Z) to score 3 (for scissors) + 3 (for draw) = 6 pts
- in total we scored 15 pts

Given we know exactly what our opponents will play (puzzle input), what would we score with the above strategy?

## Solution

### Brute-force

Seems like a lot of what-if-else or switch statements? 

```
if 'A':
    if 'X':
        res = tie
    ...
if 'B':
    if 'X':
        res = lose
    ...
if 'C':
    if 'X':
        res = win
    ...
score = score_dict[res]
```

Another way to brute-force is to pre-calculate all combinations, of which there are only 9, and score accordingly

Could generalize such that a general strategy can be submitted as input, then calculate score for all possible combinations, and map the input list using the score dictionary    

Answer: 14163

### Execution

- Our choice is always the last char per line, one of `{X, Y, Z}`
- Map that to `{1, 2, 3}` since that returns a flat score
- Result depends on opponent's choice, the last char, one of `{A, B, C}`
- Here we calculate all combinations, and create score_dict
  - `AX`: 3, `AY`: 6, `AZ`: 0, etc.

## Part 2 - New strategy

Turns out the second column of XYZs denote not what we should play, but the intended results, `{lose, draw, win}`. 

### Solution II

The second column alone tells us the result score, and from the result we have to determine what was played in order to determine the flat score.

Answer: 12091
