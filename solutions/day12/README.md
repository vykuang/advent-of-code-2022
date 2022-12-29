# AoC 2022 Day 12 - Hill climb

Get to the high ground! In a letter coded ascii map, `a` is the lowest, `z` the highest. `S` is current location, and `E` the location for best signal.

Sample map:

```
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
```

## Constraints

- Start from `S`, get to `E`
- Do so in as few steps as possible
- Each step can only move one unit higher or lower
  - e.g. if current level is `m`, we can only go as high as `n`, but not `o`
  - however there is no limit for going down; `m` has access to `a`
- Can move in the 4 cardinal directions, but not diagonal

With these constraints, the sample problem can be solved in 31 steps

## Solution one

Here we have another grid system problem, with route finding flavours.

Naive implementation:

1. Start from `S`
1. Take note of possible routes; from the corner there could be 1 or 2
1. Take one, prioritizing the higher node
1. Once we're out of the edges, there should be 1-3 options
1. Repeat until it reaches `E`
1. Return to most recent node that branched, and take the next candidate move
1. Proceed until it reaches `E`
1. Continue until all routes exhausted? How do we know all routes are exhausted?

Start from `E`?

1. Look for nodes that are equal or one lower
1. Take note of all possible branches
1. Once one reaches `S`, move onto to the next

This looks like a tree search

## Tree traversal algorithms

Two broad categories:

- depth-first: start with root node, and visits all the nodes of a branch as deep as possible before backtracking
- breadth-first: starts with root node, and visits all possible child nodes at current depth before moving to next depth

### Inorder traversal

common depth-first search (DFS) variant.

- start from root
- go to left node
- repeat until leaf
- collect the node
- backtrack to previous
- take next possible path
- nodes are not *collected* until all children are collected

### Preorder traversal

- start from root
- visit node
- go to left
- go to right

This effectively collects nodes as it works its way down, and right from the left

### Postorder traversal

- start from root
- go to left
- go to right
- collect node

### Level order traversal

Breadth-first approach (BFS). Use a FIFO queue to collect the children of nodes at each depth, so that we know the order in which to visit them

Looks like popular solutions touched on the following concepts:

- BFS
- flood-fill (intuitive but non-optimal)
- dijkstra's algorithm
- A\* algorithm
- Reversing the path
- using complex numbers (again) to represent grid coordinates
