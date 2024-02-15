# Day 21 - The monkey strikes back

## Implementating the game logic

- start at line 1, if `int`, store in `seen[mnk]`
    - if `op`, search the monkeys in `jobs`
    - repeat until `int` or in `seen`
    - look for second monkey
    - repeat until `int`
    - exec 
    - store in `seen`

### part two - solving for humn

brute-force seems unfruitful, after checking -60k - 60k. Check whether `humn` affects both or only one value

Only left changes; can we programmatically solve? How about the secant method

- given the value on the right
- given the op for value on left
- zero fn: v1 op v2 - vright = 0

The linearity of the equation allows secant to solve it 3 steps
