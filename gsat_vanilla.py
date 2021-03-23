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
                var_scores = self._get_flipped_vars_scores()
                p = self._get_var_with_best_score(var_scores)
                print(p)
                self._interpretation = self._flip_var(p)
        return None

    def _get_var_with_best_score(self, var_scores):
        best_score = var_scores[0]
        index = 0
        for i in range(1, self._formula.num_vars):
            score = var_scores[i]
            if best_score < score:
                best_score = score
                index = i
        return index + 1

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

    def _get_flipped_vars_scores(self):
        scores = [0 for _ in range(self._formula.num_vars)]
        for val in self._interpretation:
            fval = -val
            for clause in self._formula.clauses:
                length = len(clause)
                for literal in clause:
                    if literal == fval:
                        break
                    else:
                        length -= 1
                if length != 0:
                    scores[abs(val) - 1] += 1   
                    #TODO: Possible modificacio: parar de contar si es supera el minim actual
        print(scores)
        return scores
    #TODO: IDEA: guardar l'ultima variable que se li ha fet flip, per a no entrar en un bucle. 
    def _flip_var(self, var):
        new_interp = copy(self._interpretation)
        new_interp[var-1] *= -1
        return new_interp

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
