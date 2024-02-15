# AoC 2022 Day 7 - no space left

Input today is a terminal output, e.g.:

```
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
```

- lines starting with `$` are commands
  - cd
  - ls
- everything else are outputs
- thus, we're starting from root, `/`, and crawling through the filesystem
- the numbers in output denote the size in bytes
  - if it's a folder, the size denote the entire folder size

The filesystem can be deducted to look like this:

```
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
```

- Find all dir with total size of <= 1e5
- Calculate sum of their total
  - example above has dir a and dir e below 1e5, and their sums are 94853 + 584 = 95437

## Solution one

Lot of parsing here

- `$ cd <dir>` - collect directory
  - `/` - root
  - any letter - deeper inside directory
  - `..` - up one level
  - How would I model this? With a tree, right? and nodes that branch to different nodes
  - build a class for trees with arbitrary number of children per node
- `$ ls` means to look for file in the current dir. Need to know what `pwd` is to make use of that
  - `dir <name>` means it's a folder, and will not have the size preceding the name
  - if it starts with a number, that's the file size, and the item is a file

### pseudo code

1. parse line; delimit by space
1. is `line[0]` cmd or output?
  1. if cmd, is it `cd` or `ls`?
    1. if `cd`:
      1. if `/`: set pwd = root
      1. if `..`: set pwd = parent
      1. if any other, create child node, traverse there, and set as pwd
    1. if `ls`, go to next line automatically:
1. look for `dir`, and add them as child nodes to pwd
1. look for numeral, and add them as child node with size and name

Answer: 1206825

## Part ii

- Total file available space: 7e7
- space needed: 3e7

1. Determine total space
1. Determine space required to achieve 3e7 free space
1. Find the dir with the smallest size that if deleted, will let us free up that space for the update

### pseudo-code

1. root.Calc_size()
1. Find free_space = 7e7 - root.size
1. free_space should < 3e7; diff = 3e7 - free_space
1. Find dir.calc_size() for all, if size > diff
1. Return minimum

answer: 9608311
