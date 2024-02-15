# AoC 2022 Day 10 - CRT clock circuits

The simple CPU supports two instructions

1. `addx V` takes two cycles to complete
  - after two cycles, the single register, `X` increases by `V`
  - `V` can be a pos/neg integer
1. `noop` completes in one cycle and does nothing

Constraints

- The register `X` initializes with value of `1`
- Signal strength = `X` * num_cycle
- interested in `ss` during 20th, 60th, and every 40 cycles after

Test answer:

1. cycle 20: 420
1. 1140
1. 1800
1. 2940
1. 2880
1. 3960

sum of the six `ss` is 13140

## Solution i

Keep track of cycle and X

- `noop` increments cycle by one
- `addx V` increments cycle by two, and increments X by `V`

What if `addx` skips over the cycle we're looking for? does that mean we can't use modulus?

1. Deal with it afterwards:

Need a way to remember the past cycle's register value *and instruction*. If cycle jumps over the target. Only need to remember if the current instruction is addx, as there's no risk of missing with `noop`

1. Deal with it when parsing instruction
    - when `addv` is encountered, see if the jump will occur
    - if yes, append the value right now
    - if not, wait for general check

### insight

check for `(cycle - FIRST_PERIOD) % PERIOD == 0`

Answer:  17940

## Part two

- Register X controls the x-pos of the sprite, 3 pixels wide; specifically x-pos of the middle pixel
  - zero-index
- screen is 40 x 6
- draw from left to right, top to bottom; zero-index
- single pixel is drawn each cycle
- 240 cycles to draw a pixel for the whole CRT
- *if sprite is positioned such that one of its three pixels is the one currently drawn, screen produces a `lit` pixel (#); otherwise screen is dark (.)*
- what are the 8 letters on the screen?

Notes

- position is zero-index, but cycle starts from 1
  - row 0: pos 0 - 39
  - consumes cycles 1-40
  - row 5 consumes cycles 201-240
- CRT draws one pixel at a time, at the position dictated by cycle
- if any one of the sprite pixel, as dictated by X - 1, X, X + 1, match the current position, draw `#`
  - if not, draw `.`

## SOLUTION ii

Now we're matching `cycle` and `val`; if pos = cycle - 1 matches any of 

- val - 1
- val
- val + 1

that position becomes `#`; otherwise it's `.`; use `row += "#"`

Increase row when `cycle % PERIOD == 0`, i.e. start a new row, `rows.append[row]; row = ""`

Before I just skipped the cycle. Now do i need to keep track of every cycle??? CRT is still drawing pixels based on pos = cycle - 1. i also appended the signal early...I think I just need to draw two for each `addx` instruction. Make a `draw_pixel` function that...

- if `val` matches pos, add `#`
- if not, add `.`
- if pos % PERIOD == 0, start new row
- `pos` is determined *during* the cycle, and instructions complete at *end* of cycle

### insight

- returning successive chunks of a list:
  ```py
  def chunks(lst, period):
      for i in range(0, len(lst), period):
          yield lst[i:i+period]
  ```
- `cycle - 1` is not always `pos` since `pos` loops back after 40
- increment cycle before drawing the second character if instruction is add
