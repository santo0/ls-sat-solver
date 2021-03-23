#!/usr/bin/python3

# Libraries
from cnf import CNF
from random import choice
from random import randint
from copy import copy

# Agafar fitxer i parsejar-lo
# Quina estructura de dades?
# De moment llista de llistes de caracters


class GSAT:
    def __init__(self, max_flips, max_tries, formula):
        self.max_tries = max_tries
        self.max_flips = max_flips
        self.formula = formula

    def solve(self):
        for _ in range(self.max_tries):
            interpretation = self.get_random_interpretation()
            print(interpretation)
            for _ in range(self.max_flips):
                if self.satisfies(interpretation):
                    return interpretation
                var_scores = self.get_flipped_vars_scores(interpretation)
                p = self.get_var_with_best_score(var_scores)
                interpretation = self.flip_var(interpretation, p)
        return None

    def get_var_with_best_score(self, var_scores):
        best_score = var_scores[0]
        index = 0
        for i in range(1, self.formula.num_vars):
            score = var_scores[i]
            if score < best_score:
                best_score = score
                index = i
        return index + 1

    def satisfies(self, interpretation):
        for clause in self.formula.clauses:
            length = len(clause)
            for literal in clause:
                if literal == interpretation[abs(literal) - 1]:
                    break
                else:
                    length -= 1
            if length == 0:
                return False
        return True

    def get_flipped_vars_scores(self, interpretation):
        scores = [0 for _ in range(self.formula.num_vars)]
        for val in interpretation:
            for clause in self.formula.clauses:
                fval = -val
                length = len(clause)
                for literal in clause:
                    if literal == fval:
                        break
                    else:
                        length -= 1
                if length == 0:
                    scores[abs(val) - 1] += 1
        return scores

    def flip_var(self, interpretation, var):
        new_interp = copy(interpretation)
        new_interp[var-1] *= -1
        return new_interp

    def get_random_interpretation(self):
        # 0 False, 1 True
        return [i if randint(0, 1) else -i for i in range(1, self.formula.num_vars + 1)]


if __name__ == "__main__":
    print("GSAT vanilla")
    cnf_path = "./benchmarks/10_20_3__1.cnf"
    cnf = CNF(cnf_path)
    solver = GSAT(20, 20, cnf)
    solution = solver.solve()
    print("SOLUTION: ", solution)
