# day 20 - decryption by mixing

Given a sequence of integers, each number is moved forward or backwards in a cyclical fashion

- The number is moved by its value
- pos: right (forward); neg: left (backwards)
- move numbers in the initial sequence ordering (take snapshot)
- when a number arrives between the last and the first (due to the circular nature), the number goes to the end of the list
- linked list?
    - fulfills the circularity
    - `Node` class can include `idx` attribute to keep track of place in sequence?
    - would involve changing thousands after every move -> quadratic time
    - use `float` instead of `int` for `idx` to allow precise insertion without affecting other nodes
    - requires `sort` to retrieve `idx` for each move
- normal list?
    - let's try to work with linked

## part 1 - grove coordinate

- look at the 1000th, 2000th, and 3000th number after the value `0`, and take the sum, after `mixing` the given sequence
- input integers are in the thousands

Algorithm

- at `n = num` of original order
- find `num` in current `seq`, at index `idx`
- relocate `num` from `idx` to `idx + num`; num can be negative
    - if `idx + num < len(order)`: `seq = seq[:idx] + seq[idx + 1: idx + num] + [num] + seq[idx + num:]`
    - elif `idx + num > len(order)`: 

### trips

- movements wrapping the list multiple times
