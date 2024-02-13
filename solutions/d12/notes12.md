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

1. start from root; mark as visited, push to queue
1. while queue:
  a. remove node from front (node `S` will be first)
  a. add node to BFS traversal order
  a. push adjacent children nodes into queue
1. if the node popped from front of queue is the one we want, i.e. `E`, return

Another wrinkle here is we need the *depth* from `S` to `E`; need a counter to keep track of the depth.

In addition, not all children nodes are *adjacent*, due to the height restriction. Only child nodes with heights <= current node + 1 can be considered.

In the end all the above describes an approach to go through the whole graph, but we want the shortest path. How will we know it's the shortest? It's just the way it is. How will we know the depth? We need to keep track of the parent of each node discovered. Once we find `E`, we just iterate through the parents to find the depth. And again, we know that when we find `E` via BFS, it will be the first possible way to reach it, and thus the shortest.

Dijkstra's algorithm adapts BFS to do so

### Dijkstra's algorithm

### Common threads in other solutions

Looks like popular solutions touched on the following concepts:

- BFS
- flood-fill (intuitive but non-optimal)
- dijkstra's algorithm
- A\* algorithm
- Reversing the path
- using complex numbers (again) to represent grid coordinates

### Insights

- finding children nodes requires knowing height in numeric
- finding `E` requires symbolic form
  - should our class include both forms? 
  - if the other is simply a dict.get, probably don't need it
  - define `find_children()` inside `path_find()`, and include `hmap` in `path_find()` args to pass into `find_children`
- use built-in `ord()` to get integer rep of a unicode character
- build a `dict` such that `grid.get(complex_coord)` returns the character
- check for edges to determine if childrens exist, not just height diff
- need a `set` to store visited coordinates
- Check height for 'E' as well
- SOURCE IS NOT AT (0, 0)!!!
  - Need to find it first

answer: 383

## Part two

Instead of considering only `S`, consider all nodes with elevation `a`: what is the shortest path amongst all the nodes with elevation `a`?

### Execution

Dijkstra's algorithm can also build a map, so if we extended our code to include the map-making portion, we can record all path lengths from `a`.

To extend, remove the `E` check, and start from `E` instead. Once our `visited` dict is complete (unvisited empty), search for the minimum distance within the `a`s

answer: 377
