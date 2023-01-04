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
