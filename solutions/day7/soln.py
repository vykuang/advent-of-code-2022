#! /usr/bin/env python
"""
Aoc 2022 day 7 - filesystem crawling
Building a tree.
/ is the root
each directory is a node
each file is a leaf
"""
import sys

def load_input(fp):
    """
    Reads in the text file at fp and returns a generator for
    each line
    """
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line
class RootNode:
    def __init__(self, name='root', size=0, children=None):
        self.name = name
        self.size = size
        self.children = []
        if children:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
        assert isinstance(node, FileNode)
        names = [child.name for child in self.children]
        if node.name not in set(names):
            # child name must be unique per node
            self.children.append(node)
            return True
        else:
            return False

    def child_exist(self, name):
        """Does this child node exist already?

        Returns bool
        """
        return name in set([child.name for child in self.children])
    
    def calc_size(self):
        """Calculates total size, including subdirectory"""


    def __repr__(self):
        return self.name

class FileNode(RootNode):
    # Generic tree node to represent our file system
    def __init__(self, name, size=0, parent=None, children=None):
        super().__init__(name, size, children)
        # add a parent link to easily traverse up
        self.parent = parent


def parse_terminal(line: str) -> list:
    """Parse each line as delimited by space

    Returns a list containing each component
    """
    return line.split(sep=" ")

def build_file_tree(lines):
    """
    Build the file tree given the puzzle input
    """
    # initialize our root
    root = RootNode()
    # our collection of nodes
    file_tree = []
    file_tree.append(root)

    for line in lines:
        args = line.split(sep=" ")
        if args[0] == "$" and args[1] == "cd":
            if args[2] == "/":
                pwd = root
            elif args[2] == "..":
                pwd = pwd.parent
            else:
                # check if this child node already exists
                if not pwd.child_exist(name=args[2]):
                    child_node = FileNode(name=args[2], parent=pwd)
                else:
                    child_node = [child for child in pwd.children if child.name == args[2]][0]
                pwd = child_node
        elif args[0] == "dir":
            child_node = FileNode(name=args[1], parent=pwd)
            if pwd.add_child(child_node):
                file_tree.append(child_node)

        elif args[0].isdigit():
            leaf_node = FileNode(name=args[1], parent=pwd, size=int(args[0]))
            if pwd.add_child(leaf_node):
                file_tree.append(leaf_node)
        else: # ls, ignore
            pass
    return file_tree

if __name__ == "__main__":
    fn = sys.argv[1]
    fp = f"{fn}.txt"
    lines = [line for line in load_input(fp)]
    tree = build_file_tree(lines)
    if fn == "test":
        for node in tree:
            print(f"{node.name}:")
            if node.children:
                print(f"{[child for child in node.children]}")
            else:
                print(f"file size: {node.size}")
