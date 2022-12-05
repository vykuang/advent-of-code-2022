# Day 1 - Part A

## Problem Statement

[Link here](https://adventofcode.com/2022/day/1)

Input consists of groups of ints; one group comprise ints on consecutive lines, and newline separates the groups:

```
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
```

Find the group with the largest sum, and return that sum

## Solution

### First thoughts

This problem has two parts

1. Parse the data into the correct groups
2. Sort the sums to find the max

### Parsing calories

Groups are separated by a newline. After each new line, store the preceding sum in a list

### Finding the max

Naively, sorting would find the max. Otherwise numpy can trivially find it.

Apparently python already has built-in `sum` and `max` functions that can operate on any iterables including lists
