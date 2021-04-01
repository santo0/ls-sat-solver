#!/usr/bin/python3

# Libraries
from cnf import CNF
from random import choice
from random import randint
from copy import copy
import os
import sys


class GASAT():
    def __init__(self, max_flips, max_tries, formula):
        self._max_tries = max_tries
        self._max_flips = max_flips
        self._formula = formula
        self._interpretation = None
        self._sat = False
    
    def solve(self):
        pass

    def print_output(self):
        pass




if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Incorrect number of arguments. Given %s. Expected 2.\n" %
                         len(sys.argv))
        sys.exit("Use: %s CNF_file" % sys.argv[0])
    cnf_path = sys.argv[1]
    if not os.path.isfile(cnf_path):
        sys.exit("ERROR: CNF file %s does not exist." % cnf_path)
    # "./benchmarks/10_20_3__1.cnf"
    solver = GASAT(100, 100, CNF(cnf_path))
    solver.solve()
    solver.print_output()