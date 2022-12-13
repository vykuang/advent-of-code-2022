# AoC Day 4 - Camp Cleanup

Elves are assigned a range of section IDs for cleanup, but the section IDs *overlap*. Elves compile a list of section assignments for each pair (the puzzle input):

```py
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
```

The ranges are inclusive

## Part one

How many assignment pairs exist where one pair fully contains the other? e.g. 4th and 5th pair on the sample list

## Solution

Check the lower and upper bound and compare with the other pair. If:

$$\text{lower}_A >= \text{lower}_B && \text{upper}_A <= \text{upper}_B$$

Then, A is completely contained by B

## Pseudo code

1. read line
1. parse into the two pairs (delimited by comma)
1. parse into lower/upper bound
1. compare if A fits into B
1. if yes, break and increment counter
1. if not, check if B fits into A
1. if yes, increment counter, and break
1. Repeat until end of file

Answer: 464

## Part two

How many pairs contain any overlaps at all?

Instead of checking for entire subset, check for partial subset.

- if a_lb >= b_lb and a_lb <= b_ub or
- if a_ub <= b_ub and a_ub <= b_lb
