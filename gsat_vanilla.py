#!/usr/bin/python3

#Libraries
from cnf import CNF
from random import choice

#Agafar fitxer i parsejar-lo
#Quina estructura de dades?
    #De moment llista de llistes de caracters
class GSAT:
    def __init__(self, max_flips, max_tries):
        self.max_tries = max_tries
        self.max_flips = max_flips

    def solve(self, formula):
        for _ in range(self.max_tries):
            interpretation = None
            for _ in range(self.max_flips):
                if self.satisfies(interpretation, formula):
                    return interpretation
                var_score = self.get_flipped_vars_scores(interpretation, formula) 
                p = choice(var_score)
                interpretation = self.flip_var(interpretation, p)


    def satisfies(self, interpretation, formula):
        raise NotImplementedError
    
    def get_flipped_vars_scores(self, interpretation, formula):#returns formula.num_vars//2 vars
        raise NotImplementedError

    def flip_var(self, interpretation, var):
        raise NotImplementedError

    




if __name__ == "__main__":
    print("GSAT vanilla")
    cnf_path = "./benchmarks/10_20_3__1.cnf"
    cnf = CNF(cnf_path)
    solver = GSAT(1, 1)
