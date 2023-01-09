# AoC 2022 Day 13 - Distress signal

## Part one

Identify how many pairs of packets are in the right order

- packet data comprise of lists and ints
- each packet always a list, and appears on its own line
- pairs of packets separated by blank line
- to know if a packet is in the right order, compare the values:
  - first is `left`, second is `right`
  - if both are ints, lower int first
  - if both are lists, compare values of list in their respective order, i.e. first of list one with first of list two, etc.
    - shorter list should be first
    - if same length, and all values are the same, check next input
  - if only one is int, convert the int to list[int], then compare as two lists
  - decision of ordering is made as soon as possible, from left to right
    - i.e. [1,1,3,1,5] and [1,1,5,2,6]
    - once comparison check reaches (3, 5), then it decides that the order is correct since 3 < 5 and the list containing 3 is ebfore the one containing 5

Identify the indices of the pairs in correct order; first pair has index 1. Return the sum of those indices. Test answer: 1, 2, 4, 6 -> 13

## Execution

- Delimiters here are `[]` and `,`
- `[` starts a new list
- `]` ends it
- `,` separates the list elements
- read two lines
- compare
- append index if order correct
