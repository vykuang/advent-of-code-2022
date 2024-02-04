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

Pass the `ngeos` list to each recursive call so that when it gets to `t=1`, append the `ngeo` count. Structure our recursive call so that it doesn't return anything, but it modifies the `ngeos` list that was passed to it

### heuristics

- at time `t`, if there was enough resources to build a robot, and it was not built, it will always be worse to build it at `t+1`
    - record what robot was enabled but not built at `t-1`
    - is it true that in all optimal paths, once we choose not to build a robot of a certain type, that type should never be built for the remainder?
        - not true; example alternates building of clay and obs robots
- if resources at the end of time `t` is more than `(t - 1) * max(mats[req])`, stop building robots for `req`
    - set to `inf`
    - if `nmats[mat] == inf`, do not build
- keep track of current `max(ngeos)`
    - prune branches if it's impossible for it to exceed the current max
    - upper bound: building 1 geode robot every minute for all remaining time
    - e.g. at t_remain = 5, current geode count = 2, and current rate = 1, if we build 1 robot from now (t=5) to t=2, `ngeo = 2 + 1 + 2 + 3 + 4 + 5 = n_curr + r_curr + r_curr + 1 + ... + r_curr + t_remain - 1 = 13`
    - might be too high, and therefore ineffective
    - take into account blueprint? No that's just running the simulation
- iterate with intent of building a specific type of robot, instead of randomly choosing

