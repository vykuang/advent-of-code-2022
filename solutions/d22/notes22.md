# Day 22 Monkey Map

- pathfinding
- open - `.`
- wall - `#`
- last line is the prescribed path
    - alternates between num and letters
    - num - num of tiles to move, unless stopped by wall
    - letter - `R` or `L`, indicating 90deg turn in either dir, in same tile
- start from top leftmost open tile, facing RIGHT
- if moving past open spaces, *wrap around to the other side* if it is open. Stop at any point when `#` is encountered

## part 1 - final destination

- take the row, col, and *facing* of last position
- rows start from 1 at the top, and count downwards
- cols start from 1 at the left
- facing: 0, 1, 2, 3 for right, down, left, up
- ans = 1000 * row + 4 * col + facing

### wraparound

- given `face`, we determine the wraparound by taking a slice of the board along that direction
    - for -1, 1, look at the row (imag)
    - for -1j, 1j, look at the column (real)
    - since the board has no `E` or `m` structure, the min/max will work
    - when facing -1/-1j, look for max
    - when facing 1/1j, look for min
- may be worth precalculating all edges prior to traversal
- board has few edges;
    - if row in this range, min = a, max = b

### traversal logic

- chk = pos + face
- if wrap, chk = wrap
- check if wall or path
- if wall, break
- if path, inc mov, update pos, next

## part 2 - cubed

the map is actually a 2D rep of an unfolded cube; there are 6 equally sized squares that make the unfolded cube. not sure how to even start
