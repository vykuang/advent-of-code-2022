# day 18 - modelling cubes in 3d plane

Given list of coordinates representing 1x1x1 cubes, find surface area. Isolated cubes will have area of 6 units, but adjacent cubes will have lower SA. The problem here is finding out which cubes are adjacent to another. If 8 cubes were stacked in a way such that it formed a 2x2 cube, its area becomes 4 per side x 6 sides = 24, from 6 x 8 = 48, if they were all isolated

Each pair of adjacent lowers total SA by 2. Find number of adjacencies, and subtract from SA of isolated cubes?

Adjacency: given `(x, y, z)` 3d cartesian coordinate, if two out of the three match, and the last is one apart, the two cubes are adjacent

Take combination of list of cube coordinates, and count adjacencies

Given a `dataclass`, use `Myclass.__annotations__.keys()` to return list of user-defined attributes

6s execution, majority in `check_adjacent`; cannot use `set` since components may share same value

## part two - trapped air pockets

the entirety of the structure contains trapped air pockets; those surface areas should not be counted as we're only interested in exterior surface area. How do we find trapped air pockets? These are coordinates that are *absent* from the input list, but are *surrounded* by the cubes in the input list