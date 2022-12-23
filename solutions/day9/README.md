# AoC 2022 Day 9 - Heads and Tails of a rope

- Tail always follows the head, never separated by more than one node. 
- After each head movement (in one of four cardinal directions), the tail always catches up so that it is adjacent.
- adjacent means
  - it is next to H
  - it is diagonally next to H
  - on same node as H

Given a list of movement instructions for H, determine the number of nodes that T has visited at least once. T and H start on the same node

## Test input

```R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
```

- U - up; 4 - H moves up 4 times
  - After first movement, H and T are still adjacent; no T movement
  - after second, H is now one node away; T moves up accordingly to be adjacent to H
  - H ends up at (0,4); tail at (0,3)
- L - left
  - after first left, H and T are still diagonally adjacent; no T movement
  - after second, H and T are no longer diagonally adjacent; T moves diagonally towards T to stay adjacent
  - after third, T moves left one node as well

## Solution one

### Naive implementation

- calculate the coordinate for T for each H movement
- take the `set` of the list of T coordinates
- determine if T is required to move by finding the manhattan distance;
  - since diagonally adjacent is still adjacent, then our manhattan distance threshold is 2
  - if `dist_m` > 2, move T
- how to determine where to move T?
  - if H is on same column/row, then increment the T's column/row
  - if H is not on same column, nor row:
    - increment/decrement T's row/col towards H's row/col
    - e.g. H @ (1,2), T @ (0,0)
    - since neither H's coordinates match T's, move both T's coordinates toward H, i.e. increment
    - T arrives @ (1, 1)
    - Need to check diff for pos/neg to determine whether we're incrementing or decrementing

### Pseudocode



