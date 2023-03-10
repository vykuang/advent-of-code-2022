# AoC 2022 Day 14 - Regolith reservoir

Rocks are coming down!

coordinates `x,y` represent the shape of the rock structure:

- x: dist to right
- y: dist down

## test input

```
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
```

Each coordinate represents a point in the path of the rock structure, and each line of input represents the whole path. The next coordinate represents the next direction, either horizontal or vertical

Drawn out, with `#` as rock and `.` as air, the above sample looks like:

```
  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
```

## Problem description

Sand comes in from `500,0`, marked by `+`. Each unit of sand falls one at a time; the next unit does not come in until the current unit comes to a stop

Sand always tries to move down, until it meets rock or sand in its downward path. 

- If it does meet, it will first try to go diagonally left
- if it is not able, it will then try diagonally right
- if neither are available, it will come to a stop
- next unit of sand starts to come down

Simulate how many units of sand comes to rest before falling past all rock structures

## Solution one

Well this seems crazy. 

The stop condition is when a unit of sand does not come to rest on sand or rock. Crux is path detection, of both rock and resting sand.

Parsing the rock structure seems to be its own beast. We do know that every new coordinate represents a change in direction, so that the path always alternates between vertical and horizontal

We can use a numpy array to model the rocks and sands; set up poetry env for aoc and install numpy

### Path parser

- Read each line and parse into lists of `x,y` numerics
- input: list of `x,y`; output: bool array of rocks
- take the `OR` of bool arrays generated from each line to create the cave map
- for each line:
  - convert to `rock_line = [x1, y1], [x2, y2], ..., [xn, yn]]`
  - each iteration involves `xy_i` and `xy_i+1`
  - `x, y = zip(*rock_line)` to transpose
  - `np.array` can straight up take `rock_line` as input, and creates an array where each row is one set of `xy`s, column 0 is `x`, and col 1 is `y`
  - manipulate as a matrix with [r1:r2, c1:c2] slice operator
- if dx, 
