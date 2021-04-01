#!/usr/bin/python3

# Libraries
from cnf import CNF
from random import choice
from random import randint
from copy import copy
import os
import sys

# Agafar fitxer i parsejar-lo
# Quina estructura de dades?
# De moment llista de llistes de caracters


class GSAT:
    def __init__(self, max_flips, max_tries, formula):
        self._max_tries = max_tries
        self._max_flips = max_flips
        self._formula = formula
        self._interpretation = None
        self._sat = False

    def solve(self):
        for _ in range(self._max_tries):
            self._interpretation = self._get_random_interpretation()
            for _ in range(self._max_flips):
                if self._interpretation_satisfies():
                    self._sat = True
                    return self._interpretation
                C = self._get_clause_not_satisfied_by_interp()
                S = self._get_vars_in_clause(C)
                b, b_var = self._get_var_min_break(S)
                prob = randint(0, 1) #! Parametizable.
                if b > 0 and prob:
                    p = choice(S)
                else:
                    p = b_var
                self._interpretation = self._flip_var(p)

        return None

    def _get_clause_not_satisfied_by_interp(self):#! Hauria de fer que agafes una clausula random, perq sino les clausules del principi tenen preferencia a ser escollides
        for clause in self._formula.clauses:
            length = len(clause)
            for literal in clause:
                if literal == self._interpretation[abs(literal) - 1]:
                    break
                else:
                    length -= 1
            if length == 0:
                return clause
        return None


    def _get_vars_in_clause(self, clause):
        return [abs(var) for var in clause]

    def _get_var_min_break(self, vars):
        #unsat_clauses = self._get_num_unsat_clauses()
        vars_break = {}
        for var in vars:
            vars_break[var] = 0
        for var in vars:
            for clause in self._formula.clauses:
                length = len(clause)
                for literal in clause:
                    if abs(literal) == var:
                        if literal != var:
                            break
                        else:
                            length -= 1
                    else:
                        if literal == self._interpretation[abs(literal) - 1]:
                            break
                        else:
                            length -= 1
                if length == 0:
                    vars_break[var] += 1
        min_var = min(vars_break, key=vars_break.get) 
        return vars_break[min_var], min_var


#despues - antes


    def _get_num_unsat_clauses(self):
        counter = 0
        for clause in self._formula.clauses:
            length = len(clause)
            for literal in clause:
                if literal == self._interpretation[abs(literal) - 1]:
                    break
                else:
                    length -= 1
            if length == 0:
                counter += 1
        return counter

    def _interpretation_satisfies(self):
        for clause in self._formula.clauses:
            length = len(clause)
            for literal in clause:
                if literal == self._interpretation[abs(literal) - 1]:
                    break
                else:
                    length -= 1
            if length == 0:
                return False
        return True

    def _get_random_interpretation(self):
        return [i if randint(0, 1) else -i for i in range(1, self._formula.num_vars + 1)]

    def print_output(self):
        sys.stdout.write("c %s\n" % sys.argv[0][:-3])
        if self._sat:
            sys.stdout.write("s SATISFIABLE\n")
            sys.stdout.write("v %s\n" % " ".join(
                [str(cl) for cl in self._interpretation]))
        else:
            sys.stdout.write("s IDK\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Incorrect number of arguments. Given %s. Expected 2.\n" %
                         len(sys.argv))
        sys.exit("Use: %s CNF_file" % sys.argv[0])
    cnf_path = sys.argv[1]
    if not os.path.isfile(cnf_path):
        sys.exit("ERROR: CNF file %s does not exist." % cnf_path)
    # "./benchmarks/10_20_3__1.cnf"
    solver = GSAT(100, 100, CNF(cnf_path))
    solver.solve()
    solver.print_output()