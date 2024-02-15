# day 17 - tetris

## part 1

## part 2 - 1 trillion blocks

has to be some cycle detection. Determine the cycle period

What does a cycle look like here? Given P as the cycle period, the height would increase by the same amount each cycle, after some initial settling time

For example the cycle may take 1000 steps to begin, and then every 2345 steps would increase the height by 3433 units. Obviously the deciding factors are the cycles of the shapes and the jet pattern, which are both fixed.

Since our height is monotonically increasing, the cycle is in how much the height increases per block.

1. x0 = f(0) = 0
1. x1 = f(1), ...
1. x_mu = f(mu), ...
1. x_lambda + mu = f(lambda + mu) = f(mu)

- mu is index of the first element in cycle
- lambda is period of the cycle
- f(x_i) calculates how much height is increased by dropping the x_i-th block

### tortoise and hare

- two pointers going through the sequence
    - tortoise goes 1 by 1
    - hare goes 2x
- repeat until tortoise == hare, at position `v`
    - at some point they will pass into the cycle, and the distance will be divisible by `lambda`, the cycle length
- leaving `hare` at `2v`, reset `tortoise` to `x0`
- move both step by step
- when `tortoise == hare`, we've reached `mu`
    - this works because at `2v`, `hare` is the same distance away from `mu` as `mu` from the beginning, where we've reset `tortoise`
    - because math
- having found `mu`, take `hare = f(hare)` until `hare == tortoise`
- `lambda + mu` ops, constant memory

### Implementation

- Need to speed up my `f()` calls for this to work
- Reduce `stack` to only exposed parts?
    - update `exposed_stack` after each drop_stack
    - makes `.isdisjoint()` faster with fewer items in the set
- hashable:
    - jet index
    - shape index
    - top profile (?)
    - height increased
- once $\mu$ and $\lambda$ are found:
    - get `ncycles`
    - get `remainder`
    - get `height_inc_per_cycle`
        - perhaps run through the cycle again
    - *replay* the remaining unfinished cycle by looking at past increases inside the cycle
    - `ht_remainder = sum(ht_incs[mu:remainder])`
    - 1514285714288
    -  857142857126



