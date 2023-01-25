# AOC 2022 - Day 15 Beacons

- Sensors and beacons are always at integer coordinates
- sensors only know the one closest beacon, in manhattan distance
  - beacons never tie in distance to sensor
- so we've got a bunch of sensor whose coordinates we know, plus the coordinates of the closest beacon
- find number of coordinates that cannot contain a beacon

## Test input

```
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
```

Resulting arrangement

```
               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....
```

- The same beacon could be the closest one to multiple sensors
- Does not necessarily reveal all beacons
- However, since a sensor only reveals the closest, we know where beacons *are not*
- for sensor (8,7), the closest beacon is (2,10)
  - man_dist = abs(dx) + abs(dy) = 6 + 3 = 9
  - there are no other beacons with `man_dist = 9` or lower
- on row=10 (zero-indexed), the 26 positions marked by `#` cannot contain a beacon:

```
                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.
```

## Part one

In row y=2000000, how many positions cannot contain a beacon?

### Solution one

#### Parsing inputs

- split by '='
- look for numerics
- first pair is sensor xy, second pair is nearest beacon xy
- how to account for ',' and ':'???
  - use regex: `re.findall('-?\d+')`
  - `-?`: zero or more '-'
  - `\d+`: one or more decimals
  
#### Crux

The problem does not ask for an exhaustive list of where beacons cannot exist, only that at this one specific row, how many positions cannot contain a beacon?

Given the large values involved it would be unfeasible to create a map that determines for every node whether a beacon can exist.

For each node at row=2e6, consider the `d_m` to each sensor, and compare to that sensor's closest beacon

- if `d_node < d_beacon` for all sensors, that node cannot contain a beacon
- if `d_node > d_beacon` for *any* sensor, it *could* contain a beacon
- problem statement excludes possibility of beacons at equal distance from any sensor

so for each sensor (38) we compare each node. How many nodes? Given a sensor detection radius that extends furthest to the right on that particular row, the *left* edge of that block is when we can stop; all nodes between that right and left edge also cannot contain beacons. 

Same goes for the opposite side; once we know the sensor that extends farthest left, the *right* edge is when we stop searching. Again, everything between that right and left edge can be considered `True`

Extending this idea, we simply need to consider the reach of every sensor as it extends to our particular row, and count the nodes between left and right. Use a hashmap (set) to account for overlaps.

So given a sensor coordinate, how to determine the detection cone at that row?

e.g. sensor at `sx, xy`, and reach is `d`. Our row is `ty`. Once our sensor reaches `ty`, our reach will have been reduced to `d_new = d - abs(ty - sy)`. Going down to `sx, ty`, the range becomes `sx - d_new` to `sx + d_new`

#### test solution

E.g. 

- sensor at (2, 2)
- closest beacon (6, 5)
- extent of reach on row 4?

1. Find d_m = 6 - 2 + 5 - 2 = 7
1. On row = sx, reach ranges from 2 - 7 = -5 to 2 + 7 = 9
1. on row = 4, `d_new = d - abs(ty - sy) = 7 - abs(4 - 2) = 5`
1. reach extends -5/+5 from sx: 2 - 5 = -3, 2 + 5 = 7
1. Thus all nodes from (-3, 4) to (7, 4) cannot contain a beacon (`True`)

However we don't really need to keep track of coordinates; if we only had the left edge, and the reach, that would be enough to find the overlaps between sensors

E.g.

- `a` reaches 10 units from -2, to +8
- `b` reaches 7 units from 4, to +11

### Pseudocode

1. Initialize left_prev, reach_prev, right_prev to the first set, and total as empty list
1. compare with first set of (left, reach) tuple
1. If left <= right_prev, and totals is not empty, overlap has been detected. Update right edge, and increment the last value in totals list by the overlap
1. Elif left >= right_prev, or totals is empty (first iter), append `reach + 1` to totals. update left_prev and right_prev. The `+ 1` includes the original left edge.
1. Check whether beacons or sensors occupy any of the nodes that were added by comparing the `.real` portion of the complex coordinate
1. Repeat step 2 for each subsequent (left, reach) tuple
1. Return sum of totals

answer: 5838453

## Part two

- Distress source has `(x, y)` coordinates between `(0, 0), (4000000, 4000000)`
- tuning freq = `4000000 * x + y`
- find tuning freq of the distress source
- there is only one position that *could* contain a beacon
- the test example, if restrained to [0, 20], could only contain a beacon at (14,11)

### Solution two

So we've found how many cannot contain a beacon...

Once an overlap ends, that's the nook where a beacon could lie. Trick is how to retrofit the constraints of (0, 4000000) onto our existing function?

If we set left_prev = right_prev = 0...

- given first set has x=-3, reach=10
- compare -3 v. 0
- -3 <= 0
- right edge >= right_prev
- update last subtotal to right_edge - right_prev

How about this: hard set left_edge = 0, and the last right edge to 4000000, if larger