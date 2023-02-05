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


```py
