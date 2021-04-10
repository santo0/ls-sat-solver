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
        self._max_flips =  1000 * (formula.num_clauses//len(formula.clauses[-1]))
        self._formula = formula
        self._solution = None
        self._unsat_set = set()

        self._count_dict = {}
        self._iterations = 0
        self._count_var_dict = {}

        #Tabu list
        self._tabu_length = int(0.01875 * formula.num_vars + 2.8125) #Values from Tabu Search for SAT paper
        self._tabu_list = []
        print(int(0.01875 * formula.num_vars + 2.8125))
    #TODO: Guardar clausula tal que es guarda les variables que surten i els seus valors. Que estigui separat. Intentar evitar l'operacio abs().
    #TODO: La idea més important és reciclar calculs. Aprofitar calculs anteriors, no fer calculs redundants. Aixó se fa creant noves estructures de dades
    #In this implementation we want to minimize num of unsat clauses, global optimum is 0.
    def solve(self):
#        for _ in range(self._max_tries):
        while 1:
            interpretation = self._get_random_interpretation()
            for _ in range(self._max_flips):
                unsat_set = self._get_unsat_clauses(interpretation)
                #unsat_set = set/conjunt, clau/valor[posicio_clausula_unsat apartir d'interpretacio]
                if len(unsat_set) == 0:#len(unsat_set) == 0, llavors la interpretacio actual es solucio
                    self._solution = interpretation
                    return interpretation
                clause_pos = self._get_clause_not_satisfied_by_interp(unsat_set)#l'agafem de unsat_set
                S = self._get_vars_in_clause(clause_pos)#tenim posicio de clausula unsat, podem aconseguir les seves variables
                b, b_var = self._get_var_min_break(S, interpretation)#Operacio cara, ficar-se amb aixo
                prob_threshold = 0.5
                if b > 0 and random.random() < prob_threshold: #Si trenca alguna clausula i dona la probabilitat, pilles una variable d'entre les q tenies.
                    p = choice(S)
                else:
                    if b_var in self._tabu_list:#Si variable escollida esta al tabu, llavors pilles una qualsevol de les altres. 
                        p = choice(S) #! Existeix el cas en que s'agafi p. Pensar si es bo o dolent que sigui aixi.
                    else:
                        if len(self._tabu_list) == self._tabu_length:#Si tabu esta ple, llavors elimino la variable que estava dins.
                            del self._tabu_list[0]
                        self._tabu_list.append(b_var)#Fico al final de la llista (FIFO)
                        p = b_var
                self._flip_var(p, interpretation)#aqui faig un copy, no faria falta, em podria estalviar cost
                #tema metriques.
                if tuple(interpretation) not in self._count_dict:
                    self._count_dict[tuple(interpretation)] = 1
                else:
                    self._count_dict[tuple(interpretation)] += 1
                self._iterations += 1

                if p not in self._count_var_dict:
                    self._count_var_dict[p] = 1
                else:
                    self._count_var_dict[p] += 1

        return None

    def _get_unsat_clauses(self, interpretation):
        unsat_set = set()
        for clause_pos, clause in enumerate(self._formula.clauses):
            length = len(clause)
            for literal in clause:
                if literal == interpretation[abs(literal) - 1]:
                    break
                else:
                    length -= 1
            if length == 0:
                unsat_set.add(clause_pos)
        return unsat_set


    def _flip_var(self, var, interpretation):
        interpretation[var-1] *= -1

    def _get_clause_not_satisfied_by_interp(self, unsat_set):
        return choice(tuple(unsat_set))  #!AIXO NO M'AGRADA


    def _get_vars_in_clause(self, clause_pos):
        return [abs(var) for var in self._formula.clauses[clause_pos]]

    def _get_var_min_break(self, vars, interpretation):#!Reduir cost d'aquesta funcio
        #!!IDEA: Crear un index de clausules. Llista on cada posicio es una llista on hi ha el index de les clausules corresponents a una variable 
        #!D'aquesta manera no hauria d'iterar per totes les clausules.
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
                        if literal == interpretation[abs(literal) - 1]:
                            break
                        else:
                            length -= 1
                if length == 0:
                    vars_break[var] += 1
        min_var = min(vars_break, key=vars_break.get) 
        return vars_break[min_var], min_var#how many breaks, correspondent variable



    '''
    O(n) s.t. n is num_var
    '''
    def _get_random_interpretation(self):
        return [i if randint(0, 1) else -i for i in range(1, self._formula.num_vars + 1)]

    def print_output(self):
        sys.stdout.write("c %s\n" % sys.argv[0][:-3])
        if self._solution:
            sys.stdout.write("s SATISFIABLE\n")
            sys.stdout.write("v %s\n" % " ".join(
                [str(cl) for cl in self._solution]))
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
    '''
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Incorrect number of arguments. Given %s. Expected 2.\n" %
                         len(sys.argv))
        sys.exit("Use: %s CNF_file" % sys.argv[0])
    cnf_path = sys.argv[1]
    if not os.path.isfile(cnf_path):
        sys.exit("ERROR: CNF file %s does not exist." % cnf_path)
    # "./benchmarks/10_20_3__1.cnf"
    '''
    solver = WalkSAT(CNF("./benchmarks/sat_cnf/45-191-3.cnf"))
    signal.signal(signal.SIGINT, signal_handler)
    solver.solve()
    solver.print_output()
    for inp in sorted(solver._count_dict.items(), key=lambda item: item[1])[-10:]:
        print(inp)
    print(len(solver._count_dict.items()))
    print(solver._iterations)
