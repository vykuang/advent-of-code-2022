# day 19 - robot factory

Shades of day 16's pathsearching; here we search for the best way to use our resources to maximize our geode count. Should we save the resources for the obs robot, or build the clay robot right now?

## pathsearching

At each junction where we have enough resource for a robot, we either consume the resources to build it, or save it for a higher tier robot. We need to compare both, for every junction. Correction, there could be enough resources to build many types of robots. A new path is spawned for each robot that could be built, plus not building any

### implementation

1. Given `nmats`, `rates`, and `time`,
    - if `t == limit`, only collect ores, and return `nmats['geo']`
1. Determine what robots can be built at the beginning of each minute - these are the available paths
1. For each path:
    1. Consume resource
    1. build robot (or don't)
    1. collect ores,
    1. increase `rates` by `built`
    1. recurse with new states `nmats`, `rates`, and `time - 1`

### heuristics

- at time `t`, if there was enough resources to build a robot, and it was not built, it will always be worse to build it at `t+1`
- if resources at the end of time `t` is more than `sum((t - 1) * max(mats[req]))`,
