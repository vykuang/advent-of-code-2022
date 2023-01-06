# AoC 2022 Day 11 - Monkey in the middle

Monkeys are tossing items back and forth.

- items are labelled by their `worry` attribute
- each monkey changes the `worry` attribute differently when they throw the item
- each monkey has a different test to determine which monkey to throw the item to
- after monkey inspects the item (changing the worry level) but before the test, the worry level is divided by 3 (since the item is okay still)
- when a monkey tosses an item, another monkey receives it as the last item on their queue
- there are `n` monkeys, each with a different `worry` operation and `toss` check

## Constraints

- get 2 most active monkeys, by looking at *the total num of times each monkey inspects items over 20 rounds*
- get the top two inspections and get the product, i.e. *level of monkey business*
- after each monkey tosses, one round has passed
- when it's the monkey's turn, they toss *all the items* in their queue

## Test input

```
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
```

Round 1:

- Monkey 0:
  - inspect item with worry=79
  - apply worry operator: worry \*= 19 = 1501
  - div by 3 = 500
  - toss test: div by 23?
    - not div -> false -> toss to #3
  - inspect item with worry=98
  - apply worry: w_new = 98 * 19 = 1862
  - div by 3 = 620 (implicit flooring)
  - toss test: div by 23?
    - not div -> false -> to #3

## Solution one

Input has the following info for each monkey:

- monkey id
- list of starting items as their initial worry attribute
- worry operation
  - save as a lambda func?
- toss test
- if true, toss to monkey a, else b

### Execution

Make a class of monkeys? Put them in a list? Make methods for them to go through a round automatically?

- for each monkey
  - worry op/toss test for all item
  - return {id: [items]}
  - `.extend()` [items] for each `id`
- repeat for every monkey
- repeat for `n` rounds

answer: 57838

## Part two

- worry no longer divided by 3 after each inspection
- worry levels will need to be kept track of another way
- rounds up to 10000

## Solution two

Instead of using the `worry_op` to multiply out the numbers, and then test divisibility, we need to find another way.

Even if rounds exceed 10000, the only ops we're concerned about is multiplication

- if not `mul`, carry out `worry_op` as usual
- if `mul`, append as list of factors???
  - what if that item has a different operation after???
- the whole reason we need to keep track of `worry` is to carry out the div test, so that we know who will receive that item- when checking divisibility, we only need to check the tail-end of a number.
  - e.g. div by 13
  - we don't need to check beyond 130,000 (as an arbitrary example)
  - to check if 194,241 is div by 13, first subtract by 130,000, and check the result: 61,241
  - these truncations will not affect plus or minus
    - but it will affect future mul/div???
- using clever div rules that are hard-coded for each number still involves knowing the initial number to begin with

### insight

- worries never actually go down:
  - only `+` or `*`
  - this preserves a property called **congruence**
- congruence is important because it allows us to truncate the worry levels
- truncate by the *product of all potential divisors*, or more generally the least common multiple
  - since all divisors here are prime, it's also just the product

answer: 15050382231

Note that using part 2 methods will return slightly different answers than part 1 methods, re: test inputs
