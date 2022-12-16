"""
Helper functions for reading input/test text inputs
"""
def load_input(fp):
    """
    Reads in the text file at fp and returns a generator for
    each line
    """
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line
