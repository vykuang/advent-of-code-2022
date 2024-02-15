# day 18 - modelling cubes in 3d plane

## part 1 - adjacencies

Given list of coordinates representing 1x1x1 cubes, find surface area. Isolated cubes will have area of 6 units, but adjacent cubes will have lower SA. The problem here is finding out which cubes are adjacent to another. If 8 cubes were stacked in a way such that it formed a 2x2 cube, its area becomes 4 per side x 6 sides = 24, from 6 x 8 = 48, if they were all isolated

Each pair of adjacent lowers total SA by 2. Find number of adjacencies, and subtract from SA of isolated cubes?

Adjacency: given `(x, y, z)` 3d cartesian coordinate, if two out of the three match, and the last is one apart, the two cubes are adjacent

Take combination of list of cube coordinates, and count adjacencies

Given a `dataclass`, use `Myclass.__annotations__.keys()` to return list of user-defined attributes

6s execution, majority in `check_adjacent`; cannot use `set` since components may share same value

### optimization

No point in checking between *all* combinations. If we're counting adjacencies, look for immediate neighbors for each node

```py
# lots of useless comparisons, automatic quadratic time
from itertools import combinations
adj = [c1.check_adjacent(c2) for c1, c2 in combinations(cubes, 2)]

# checking immediate neighbors only
sa = sum([len(cube.sides() - cubes) for cube in cubes])
```

- `cube.sides()` generates a set of neighbors
- `set - others` returns all items in `set` *but not* `others`
- `len(cube.sides() - cubes)` counts how many sides are *not lava* and are exposed to air
- sum all sides exposed to air

## part two - trapped air pockets

the entirety of the structure contains trapped air pockets; those surface areas should not be counted as we're only interested in exterior surface area. How do we find trapped air pockets? These are coordinates that are *absent* from the input list, but are *surrounded* by the cubes in the input list

- Given list of droplet coordinates, search for empty pockets within the bounds
- Once all coords of empty pockets are known, apply part 1 function to find the empty pockets surface area
    - assume there are no lava droplets within air pockets
- subtract air pocket surface area from part 1 answer

### searching for air pockets

```py
pockets = []
    zmin, zmax = find_min_max(cubes, 'z')
    for z in range(zmin + 1, zmax):
        fixed_z = {cube for cube in cubes if cube.z == z}
        ymin, ymax = find_min_max(fixed_z, 'y')
        for y in range(ymin + 1, ymax):
            fixed_y = {cube for cube in cubes if cube.y == y}
            xmin, xmax = find_min_max(fixed_y, 'x')
            for x in range(xmin + 1, xmax):
                # look for air pockets
                if (pocket := Cube(x, y, z)) not in cubes:
                    pockets.append(pocket)
    pockets_adj = [p1.check_adjacent(p2) for p1, p2 in combinations(pockets, 2)]
    psa = 6 * len(pockets) - 2 * sum(pockets_adj)
    sa -= psa
```

Runs into problems with `M` shaped droplets, or concave shapes. The above only works for convex droplets. With concave, it will count areas reachable by water as air pockets.

### flood-fill

Starting from some known non-lava coordinate close to the droplet, bounded by the min/max of known droplet coordinates, search for all lava surfaces reachable.

Naive flood fill:

```py
todo = deque()
todo.append(source)
while todo:
    node = todo.popleft()
    if node is inside:
        # process the node

        # 6 direc flood fill; either dir in x, y, z plane
        for direc in [...]:
            todo.append(node + direc)
```

optimizations

- check child nodes before appending
- use loop for east/west, queuing pixels above/below