# AoC 2022 Day 5 - Supply Stacks

Supplies are in marked crates, unloaded from ships. To get the ones we need, they have to be rearranged. A giant cargo crane moves crates between the stacks, so the desired crates come on the top.

Input: 

1. initial stacks of crates
```
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3
 ```

1. rearrangement procedure

```
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
```

After step 1:

```
[D]
[N] [C]
[Z] [M] [P]
 1   2   3
```

After the 4 steps:

```
        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
```

Note that because crates are *moved one at a time*, when multiple crates are moved their orders are reversed

## Part i

Given initial schematic and set of procedures, find which crates end up on top

### Solution - i

hmmmm.

Things to parse

- crate schematic
  - stack number (variable)
  - crate ID
- stack procedure
  - number of crates
  - from which stack
  - to which stack

The way these stacks work is identical to the compsci stack: last in first out (LIFO).

Python library has these built-in structures:

- list
  - scaling issue with larger size
  - designed for random access
- collections.deque
  - aka "deck", for double-ended queue
  - more optimized for access-at-ends, via doubly-linked list: each element has references to the previous and next only
  - obv slower for random access: `myDeque[3]` requires walking through the entire stack
  - constant time for `.append()` and `.pop()`
- queue.LifoQueue
  - thread-safe variant of `deque`

All will have the `.append()` and `.pop()` method to model our stacks

### Pseudo code

- parse the stacks into a corresponding number of `deque`s
- parse instructions into `.append()` and `.pop()` statements
- iterate the instructions
- call `.pop()` on all `deque`s to find the final sequence of top crates

### Execution log

- use `str.isdigit()` or `str.isalpha()` methods to discern numerals and letters
- `list.index()` only works as intended for unique characters
  - input had two Gs and Cs on the same row, and confused my initial attempt to log position using `.index()`
- cannot change dict while iterating over it

Answer: JCMHLVGMG

## Part two

The cratemover isn't doing what we want! It's the wrong model! Turns out it *can* move multiple crates at once, instead of one at a time like we thought. Moving multiple crates means they stay in the same order

### Solution two

Original implementaion forced `.pop()` and `.append()` one at a time in a `for` loop. Now that we are not constrained by LIFO, a list makes more sense than deque.

However I don't want to refactor deques into lists, so I'll use the `reverse()` method before `.extend()`

answer: LVMRWSSPZ
