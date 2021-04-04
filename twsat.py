#!/usr/bin/python3

# Libraries
from cnf import CNF
from random import choice
from random import randint
import random
from copy import copy
import os
import sys, signal

# Agafar fitxer i parsejar-lo
# Quina estructura de dades?
# De moment llista de llistes de caracters
      


class WalkSAT:
    def __init__(self, formula):
#        self._max_tries = max_tries
        self._max_flips =  100 * (formula.num_clauses//len(formula.clauses[-1]))
        self._formula = formula
        self._interpretation = None
        self._sat = False

        self._count_dict = {}
        self._iterations = 0
        self._count_var_dict = {}

        #Tabu list
        self._tabu_length = int(0.01875 * formula.num_vars + 2.8125) #Values from Tabu Search for SAT paper
        self._tabu_list = []
        print(int(0.01875 * formula.num_vars + 2.8125))

    #TODO: La idea més important és reciclar calculs. Aprofitar calculs anteriors, no fer calculs redundants. Aixó se fa creant noves estructures de dades
    #In this implementation we want to minimize num of unsat clauses, global optimum is 0.
    def solve(self):
#        for _ in range(self._max_tries):
        while 1:
            self._interpretation = self._get_random_interpretation()
            for _ in range(self._max_flips):
                if self._interpretation_satisfies():
                    self._sat = True
                    return self._interpretation
                C = self._get_clause_not_satisfied_by_interp()
                S = self._get_vars_in_clause(C)
                b, b_var = self._get_var_min_break(S)
                prob = random.random() 
                if b > 0 and prob < 0.5: #! Parametizable.
                    p = choice(S)
                else:
                    if b_var in self._tabu_list:
                        p = choice(S) #! Existeix el cas en que s'agafi p
                    else:
                        if len(self._tabu_list) == self._tabu_length:
                            del self._tabu_list[0]
                        self._tabu_list.append(b_var)
                        p = b_var
                self._interpretation = self._flip_var(p)
                if tuple(self._interpretation) not in self._count_dict:
                    self._count_dict[tuple(self._interpretation)] = 1
                else:
                    self._count_dict[tuple(self._interpretation)] += 1
                self._iterations += 1

                if p not in self._count_var_dict:
                    self._count_var_dict[p] = 1
                else:
                    self._count_var_dict[p] += 1

        return None

    def _flip_var(self, var):
        new_interp = copy(self._interpretation) #costos
        new_interp[var-1] *= -1
        return new_interp

    def _get_clause_not_satisfied_by_interp(self):#! Hauria de fer que agafes una clausula random, perq sino les clausules del principi tenen preferencia a ser escollides
        unsat_clauses = []
        for clause in self._formula.clauses:
            length = len(clause)
            for literal in clause:
                if literal == self._interpretation[abs(literal) - 1]:
                    break
                else:
                    length -= 1
            if length == 0:
                unsat_clauses.append(clause)
        return choice(unsat_clauses)


    def _get_vars_in_clause(self, clause):
        return [abs(var) for var in clause]

    def _get_var_min_break(self, vars):
        #unsat_clauses = self._get_num_unsat_clauses()
        vars_break = {}
        for var in vars:
            vars_break[var] = 0
        for clause in self._formula.clauses:
            length = len(clause)
            for var in vars:
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


    '''
    O(n) s.t. n us num_clauses
    '''
    def _get_num_unsat_clauses(self):
        num_unsat_clauses = 0
        for clause in self._formula.clauses:
            length = len(clause)
            for literal in clause:
                if literal == self._interpretation[abs(literal) - 1]:
                    break
                else:
                    length -= 1
            if length == 0:
                num_unsat_clauses += 1
        return num_unsat_clauses

    '''
    O(n) s.t. n is num_clauses
    '''
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

    '''
    O(n) s.t. n is num_var
    '''
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


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    for inp in sorted(solver._count_dict.items(), key=lambda item: item[1])[-10:]:
        print(inp)
    for vareto in sorted(solver._count_var_dict.items(), key=lambda item: item[1])[-10:]:
        print(vareto)
    print(len(solver._count_dict.items()))
    print(solver._iterations)
    sys.exit(0)

if __name__ == "__main__":
    global solver
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Incorrect number of arguments. Given %s. Expected 2.\n" %
                         len(sys.argv))
        sys.exit("Use: %s CNF_file" % sys.argv[0])
    cnf_path = sys.argv[1]
    if not os.path.isfile(cnf_path):
        sys.exit("ERROR: CNF file %s does not exist." % cnf_path)
    # "./benchmarks/10_20_3__1.cnf"
    solver = WalkSAT(CNF(cnf_path))
    signal.signal(signal.SIGINT, signal_handler)
    solver.solve()
    solver.print_output()
    for inp in sorted(solver._count_dict.items(), key=lambda item: item[1])[-10:]:
        print(inp)
    print(len(solver._count_dict.items()))
    print(solver._iterations)