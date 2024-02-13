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

This type of sorting effectively compares the lists as if they were just two numbers:

- [1,1,3] = 113, [1,1,5] = 115, and 113 < 115, so list 1 should be first
- [[1],[2,3,4]] vs [[1],4]
  - 1 == 1234
  - 2 == 1400
  - 4 became 400 because we're comparing it to [2,3,4] == 234
  - 1 should be first
- [[4,4],4,4] vs [[4,4],4,4,4]
  - first pair is same
  - 4, 4 == 44; 4, 4, 4 == 444
  - 1 should be first
- [[[]]] vs [[]]
  - my logic kind of breaks down here
The 2nd example also shows that in this implementation, the value changes in the context of the other list

### insight

- `eval` can parse "[1,2,[3,4,5,],5]" into an actual python list object
  - it's designed to dynamically evaluate python expressions
  - because of the dangers associated with executing dynamic and arbitrary code, there is `literal_eval` from `ast` library which only evaluates python literals into objects, and does not support operators
- split by `\n\n` since the pairs are separated by a blank line
- recursively compare until we end up with int-int
- use `match-case` to determine if we're comparing ints or lists
- enumerate has a `start` argument, so we can start our index at 1
  
### Pseudocode

1. left = first packet; right = second packet
1. if left == int and right == int, return left - right
1. elif left == int and right == list, convert left to list and compare the two lists. vice versa for right
1. else both are lists:
  1. for each element in list, compare (as in step 1)
  1. if any are different, return the result
  1. else if all are same, then one list should run out of items first
  1. at which point compare the length of the lists as int-int

answer: 5843

## Part two

Given we can sort the packets in pairs, we now must sort all the packets.

In addition, two packets must be inserted:

- `[[2]]`
- `[[6]]`

Return the indices of their proper placements, as their product. Index starts at 1.

## Solution two

Naive - read input as before, then append the dividers. Do not split by `\n\n`, only `\n`? After sorting, search for our dividers' indices

Count - count how many would be placed before `[[2]]` - `n + 1` will be the first index; how many would be placed before `[[6]]`? `m + 2` will be the second index. Product = `m*n + 2*m*n + 2`

Re-purpose our `cmp()` func to sort via `sorted` and `functools.cmp_to_key`

### Primer on `sorted`, `key`, and `cmp_to_key`

Usually, `sorted()` takes a `key=` arg which returns an absolute value for purpose of sorting. e.g. sorting a tuple, and we want to sort by the `[1]`th value instead of the first

Alternatively, instead of returning absolute vals, we can supply a callable `compare()` function which returns negative, equal, or positive based on comparison result. Since `sorted()` only has the `key` arg, python has provided a `cmp_to_key` feature to allow use of a `cmp()` func.

Thus we can sort all packets using the `cmp()` func built in part one:

```
sorted(packets, key=functools.cmp_to_key(cmp))
```
### Execution

Counting is easier. Reuse our `cmp()` and compare `[[2]]` and `[[6]]` against all packets, and count the results

answer: 26289
