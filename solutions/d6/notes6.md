# AoC 2022 Day 6 - Tuning trouble

## Part one 

Fix the comms! Add a subroutine that detects a *start-of-packet marker*. Here, the marker is a sequence of *four chars that are all different*.

Identify the first pos of that marker sequence, and report num of chars from beginning of buffer to the end of the first marker

Test:

```
mjqjpqmgbljsphdztnvjfqwrcgsmlb
```

The earliest first marker is after the 4th char, and first potential marker sequence is `mjqj`, but because `j` is repeated, this is not the correct sequence.

The correct first sequence is after the 7th char has been received, starting with the 4th char: `jpqm`, all unique letters. Thus we should report back `7`, since that is the end pos of the first parker

### Solution one

Use a `deque()` keep track of the candidate marker sequence. Use `.append()` and `.pop()` to iterate through the data stream

Check for two things

- new char is not in current candidate sequence
- set(window) length < window

answer: 1531

## Part two

Start of packet sequence is 4 unique chars; *start-of-message sequence* is 14 unique chars. Find the position of the end of that sequence.

### Solution two

Parametrize `seq_len` to 14
