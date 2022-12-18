# AoC 2022 Day 8 - treehouse

Are there enough trees to keep a treehouse hidden? See grid of tree heights (puzzle input):

```
30373
25512
65332
33549
35390
```

- 0 is shortest
- 9 is tallest
- tree is *visible* if all trees between it and an edge of grid are shorter
- only look up/down/left/right
- all trees on the edge are by default *visible*
- only interior 9 trees (3 x 3 grid) to consider in the example
- total of 21 trees are visible in the above grid

## Part one

How many trees are visible in our grid?

### Solution one

- count `line_length` and `num_lines`
  - edge_trees = 2 * (line_length + num_lines - 2)
- check each interior tree for visibility
  - visibility has 4 directions: up/down/left/right
  - for each node, collect all the trees between it and the edge - 4 collections
  - if max(collection) < node.height, node is visible in that direction
  - node only needs visibility from one direction to count as *visible*
- count number of visible trees

This doesn't scale particularly well. Since we're looking only for visibility, perhaps we can analyze the grid row-wise, and then column-wise.

- for each line, find all *visible* nodes
- for each column, within the pool of row-wise visible nodes, look again for visible nodes

But is there another way of finding visible nodes? Is this problem transposable to finding the local maximums on a 2d plane? No since visibility can be earned from 4 directions

- find all nodes visible from left or right
  - take an interior row
  - get the max
  - find first occurrence of max from left:
    - all nodes on the left are non-visible from right
  - find first occurrence of max from right:     
    - all nodes on right are non-visible from left
    - all nodes inbetween are non-visible from neither left nor right
- repeat for up/down

Since the constraint for visibility is more lax than *invisibility*, perhaps it's more efficient to check for that instead. Node is only invisible if it is not visible from any cardinal directions

I think we could extend the idea of using `max` to determine visibility by successively finding it.

- find first array max from *right*
  - This mitigates issue where equivalen max values are found
  - if equal, trees are not visible; need to be higher
  - reverse, then `.index()`
- set left side `invis_from_right`
- to look for others that may be `invis_from_right`, look for next `max`, excluding current `max`. Once found, all nodes between new max and prev max are marked `invis_from_right`, if any.
- iterate until idx at end of line
  - expect visible trees to be more frequent towards the right? not necessarily
- do so for all rows.
- repeat to find max from right, to mark nodes as `invis_from left` from max to right most start
- *marking* is done by creating a boolean array? end goal here is to use `OR` operation between four bool arrays to find all visible nodes, then sum to count
  - given the idx of `prev_max` and `current_max`, set them invisible by appending `False` to an ongoing list.
  - set each `max`s as visible by appending `True` to the list, such that the idx in the list corresponds with the grid pos
- surely I can't save m x n objects, each with four properties 

`find_visible` only works for `vis_right`; how do I make it work for `vis_left`?

- reverse the input
- setup is the same
  - prev_max set as left-most height; since input was reversed, this is actually the right-most height
- never mind it works, I just set the index increment logic wrong
  - `idx += num_vis + 1`; the `+ 1` is required to move past current max, and `num_vis` is the index relative to `idx`

## Part two

Now we're looking for the highest *visibility from each tree* instead of from the edges of the forest. Visibility is determined by visibility in each of the four cardinal directions, multiplied together.

- Tree of height 5 can see up to and including another tree of height 5, but not past that.
- Find the highest vis score for our tree map

### Solution two

Oh boy. Can we re-use any of our existing code?

Let's look at it from a blank slate. How would one solve this problem from the beginning?

### Bruce-force

- Consider every node
- Gather array for each direction
- Look for nearest node that is equal or taller
- Difference in pos is the vis_score
- Product is scenic_score

### A smarter way?

We're essentially lookin for the highest product of the vis_score. In any case there would be four matrices, one for each direction. Difference is how to build one. Do every node have to be considered?

Don't see a way around it.
