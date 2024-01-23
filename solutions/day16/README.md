# AoC 2022 Day 16 - Volcanos

More graphs and data structures.

So we've got tunnels and valves to open. What's the optimal path?

## Graphs

Here we have an *undirected weighted cyclic graph*:

- *directed graph*: graph comprising of vertices connected by directed edges, or arcs. aka *digraph*
  - edges are directional
  - some nodes may still be bi-directional, if they have one edge `A -> B` and another `B -> A`
- we have an *undirected* graph: nodes can lead to any adjacent nodes with no regard for backward/forward.
  - all edges are two-way, or *undirected*
- nodes are able to form a non-empty *cycle*
  - cycle: non-empty trail in which only the first and last vertices are equal
  - *directed* cycle in a directed graph: non-empty *directed* trail in which only the first and last vertices are equal
  - opposed to *acyclic*, or DAG, which cannot form cycles
    - see Airflow
- *weighted*: there is a cost associated with traversing from one node to another
    
## Insights

- compress the graph by skipping over 0 release valves
  - AA - BB - CC
  - if BB has release=0, don't count AA - BB - CC; shorten to AA - CC with length=2
  - don't consider AA - BB - AA as candidate
- *dynamic programming*
  - *optimal substructure*: solution to a given optimization problem can be obtained by the *combination of optimal solutions* to its *subproblems*.
    - substrctures often described by recursion
    - e.g. finding shortest path between two vertices
    - if path `p` from `u` to `v` is truly the shortest, then the path can be broken down to `p1` and `p2` at midpoint `w` such that `p1: u -> w` and `p2: w -> v` are also the shortest
  - *overlapping subproblems*: subproblem space is *small* such that any recursive algorithm should be solving the same subproblem repeatedly
    - dynamic programming solves each sub-problem only *once*
    - e.g. fibonacci sequence
  
## Solution one

### Naive

Depth-first search on all possible paths that can be taken in 30 minutes, and calculate the pressure released for each path

- collect all paths at depth=30
- record pressure released as we iterate down each path

How to record pressure? Record, for each path, a dict: `{valve_id: time_release}`. At the end of the path, at depth=30, calculate the total pressure released by cross-referencing the `tunnel[valve_id].rate`. More intuitively, record `time_remaining` instead of `release` to do a simple multiplication with rate. Thus the scoring func becomes

```py
def score(valve_time: dict, tunnels):
    tot = 0
    for valve in valve_time:
        tot += valve_time[valve] * tunnels[valve].rate
    
    return tot
    

# with functools
from functools import reduce
tot = reduce(
    lambda subtot, valve: subtot + valve_time[valve] * tunnels[valve].rate, 
    valve_time, 
    0)
```

To collect all paths within depth=30, can use any of the depth-first search traversals

- start at vertex `s`
- *visit* vertex `s`
- `s` is now current vertex `u`
- travel along arbitrary edge `(u, v)`
- if `v` is already visited, return to `u`
  - travel to a different edge
  - if all edges are travelled, backtrack to another previous vertex
    - need to keep track of explored edges for each vertex?
- if not, *visit* `v`, set as current, and travel to arbitrary edge

DFS runs in `O(n_s + m_s)` time; stores graph in an adjacency list: for each node, store a list of adjacent neighbor nodes.

[see here for animation](https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/GraphTraversal.html)

### Implementing the graph

Because we're collecting all *paths*, not just all the valve nodes (which we already know), we're not simply running DFS on the valve nodes, we're running DFS on all the *different paths that can be taken*.

From vertex `s`, in our case, *all nodes are accessible*, with varying time costs, or weights, associated with the arcs. At every child node, all *unvisited* nodes are also accessible, if `total_time < time_limit` 

DFS on all the different *paths* will return an exhaustive list of all possibilities, by design

As a prerequisite, this approach needs to know the shortest path between every pair of points. Use dijkstra to build the adjacency list, by starting from every vertex as origin:

```py
adj_list = {
    "A": {"B": 2, "C": 3, ...},
    "B": {"A": 2, "C": 1, ...},
    ...
}
```

### Dijkstra (again)

1. mark all nodes `unvisited` in a set
1. assign to origin node a distance of 0, and all other nodes a tentative distance of `infinity` since they are not known yet. set initial node as current
1. at current node, consider all unvisited neighbors
  - assume we know the distances between all neighboring nodes
  - `new_tentative_dist = current_node_dist + neighbor_dist`
  - if `dist[neighbor] > new_tentative_dist` then update: `dist[neighbor] = new_tentative_dist`
1. after considering all *unvisited* neighboring nodes, mark current node as `visited`, and remove from `unvisited` set
1. If the target node has been marked as `visited`, or if the smallest tentative dist among unvisited nodes is `inf` (occurs when there is no conn b/w initial noe and remaining unvisited???), algorithm has finished
1. else, repeat from 3
  - pop the node from `unvisited` set with smallest tentative dist, and set as current
  - consider all neighbors...

### Floyd-Warshall

Alternatively, use *Floyd-Warshall* for a dense graph, where most or all pairs are connected

`scipy.sparse.csgraph` has `floyd_warshall` and `dijkstra` predefined, as does `networkx`

- scipy requires adjacency matrix:
  - in a graph with vertex set $U = {u_1, u_2, ..., u_n}$, adj_mat $A$ is a $n x n$ matrix
  - $A_{ij}$ represents the distance between $(u_i, u_j)$
  - 0 means no connection
- we would need another dict to map the integer index to the name of the valve, `{valve_id: valve_index}` in order to represent as adjacency matrix

### DFS

Having built a dict of shortest paths for each point, now we collect each possible path and score them.

From the start, all nodes are accessible, and remain accessible unless

- a node has already been visited *in this path*, or
- the current time + distance + valve opening time >= time_limit (30)

How do we keep track whether a node has been visited *in this path*? The same node can be part of different paths, but it cannot be in the same path more than once.

- keep hash of paths?

In graph terminologies, we are looking for all **simple paths**: paths without repetition of vertices. *Non-simple* paths are those that include **cycles**, e.g. 1-3-1-4

### Path-finding pseudo code

Modifications to fit our volcano tunnels in bullet points

- start from source vertex `s`; initialize as `current_path`, since it starts empty
- check if neighbor `a` is in `current_path`
  - neighbors are all nodes in graph not in `current_path`
  - by this logic the check is redundant
  - additional check: compare distance between current node and neighbor:
    - if `time_remain + dist + 2 <= time_lim`, then it is viable
    - else, even if we reach the valve and open it, there will not be enough time for the valve to count towards the total release.
    - e.g. time_remain = 20, dist = 9; reach node at t=29, valve opens by t=30. time_open = 0
- if pass, append to `current_path`
  - also record `time_release = time_lim - time_remain`
- from node `a`, check neighbor `g`
- if pass, append `g` to `current_path`, and set `g` as current
- from `g`, check `j`
  - `a`, `s` are already in `current_path` and therefore not considered
  - `j` does not pass due to time_limit
    - `time_remain + dist[g][j] + 2 > time_lim`
- return to `g`, check `k`, and remaining neighbors
  - none meets the time limit
- `s - a - g` is our path
- return `[s: t1, a: t2, g: t3]`
- how do I backtrack back to `a`, to check `j`, `k`, etc.?
  - `yield` and `yield from` takes care of that

### similarity to knapsack problem

Given a knapsack that can hold 35 kg, what do you take to maximize value? Different approaches:

- greedy: take the most valuable first
    - however, this might miss more optimal approaches of taking more quantities of lesser valued items

This is more akin to the traveling salesman problem: how do you travel between all the nodes in the shortest amount of time? This is an NP-complete problem

### bfs

Return (or yield) all possible paths that fit in the 30 min mark

Don't think I can call this breadth-first search. Use `yield from` for all general cases, and `yield` for base case in recursion

### part two - elephant in the room

Instead of adding one, add two `(cave, time_remain)` to `path`, one for human, and one for elephant. 

Add cave to human path as usual, from available pool. Then, from that same pool, choose cave for elephant, *taking into account where the elephant came from*. Only after appending two cave tuples do we recursively call the next level.

Keep current cave and time_remain for both elephant and human

Do we need to move on from the `for cave in working_valves` structure, if we need to choose two?

And about what the asynchronous nature of the two agents moving through the tunnels? H could very well reach two in the time it takes for E to reach one

### step by step

1. Both start @ `AA`
1. H chooses `JJ`, so E chooses `DD`
1. E to `DD`, taking 2 min for travel and open
1. H to `JJ`, taking 3 min for travel and open
    - at this time, E is already moving toward another valve

I think they have to be separate paths, with their own timer, but the two need to be cognizant of each other's progress to not repeat

If each path picks new valves each turn, they could desync; one could use up too much time compared to the other. Is that a problem? If they both use up the time allotted, I don't see how.

From above:

1. From 2, there are branches for each valve H chooses; within that branch E chooses a corresponding different valve as well
    - implies a `for each valve` loop when adding valve
1. 

Programming gets really tricky here. We could reuse part 1, save all the sets (and respective sum), and look for all pairs of *disjointed sets*, so that human and elephant can traverse the two paths, and look for the max.

### optimization

naive brute-force would have us comparing $50,000^2$ pairs, given 50,000 different paths in the time limit. To trim down the search space:

- sorting
- compare only paths with a certain threshold of valves opened

see [example](https://github.com/davearussell/advent2022/blob/master/day16/solve.py)