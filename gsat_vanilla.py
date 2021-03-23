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
            for _ in range(self.max_flips):
                if self.satisfies(interpretation):
                    return interpretation
                # list of values 1 to n : n is number of variables
                var_scores = self.get_flipped_vars_scores(interpretation)
                #print(var_scores)
                #p = choice(var_scores)
                p = randint(1, self.formula.num_vars)
                interpretation = self.flip_var(interpretation, p)
        return None

    def satisfies(self, interpretation):
        #print(interpretation)
        #print(self.formula)
        for clause in self.formula.clauses:
            sat_clause = False
            #print(clause)
            for literal in clause:
                pos = int(literal.lstrip('-')) - 1
                interp = interpretation[pos]
                if literal[0] == "-":
                    literal_value = 0
                else:
                    literal_value = 1
                sat_clause = sat_clause or (interp == literal_value)
                #if interp != literal_value:
                    #print("Fails on %i (%s)" % (interp, literal))
            #print("BYE")
            if not sat_clause:
                #print(clause, interpretation)
                return False
        return True

    def get_flipped_vars_scores(self, interpretation):
        scores = [0 for _ in range(self.formula.num_vars)]
        for pos, val in enumerate(interpretation):
            for clause in self.formula.clauses:
                sat_clause = False
                for literal in clause:
                    var = int(literal.lstrip('-'))
                    if var == pos + 1:
                        if literal[0] == "-":
                            literal_value = 0
                        else:
                            literal_value = 1
                        sat_clause = sat_clause or (
                            ((val + 1) % 2) == literal_value)
                if not sat_clause:
                    scores[pos] += 1
        return scores

    def flip_var(self, interpretation, var):
        interp = copy(interpretation)
        #print(var)
        interp[var-1] = (interp[var-1]+1) % 2
        return interp

    def get_random_interpretation(self):
        # 0 False, 1 True
        return [randint(0, 1) for _ in range(self.formula.num_vars)]


if __name__ == "__main__":
    print("GSAT vanilla")
    cnf_path = "./benchmarks/100_400_3__1.cnf"
    cnf = CNF(cnf_path)
    solver = GSAT(100, 100, cnf)
    solution = solver.solve()
    print("SOLUTION: ", solution)