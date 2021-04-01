#!/usr/bin/python3
# MUST USE <= PYTHON3.6


# Libraries
from cnf import CNF
from random import choices
from random import randint
from random import random
from functools import reduce
from copy import copy
import os
import sys


'''
Genetic Algorithm for SAT solving

Based on: https://www.astesj.com/publications/ASTESJ_020416.pdf
'''


class GASAT():
    def __init__(self, max_gen, formula):
        self.formula = formula
        self.solution = None

        self.ELITISM_RATE = 0.2
        self.MAX_GEN = max_gen
        #self.TOTAL_GEN = 1
        #self.CURRENT_GEN = 1
        #self.MAX_FITNESS = 0
        self.POP_SIZE = self.formula.num_vars
        self.LAST_GEN = None

    def solve(self):
        while 1:  # while 1 in production
            population = self.create_random_population()
            for _ in range(self.MAX_GEN):
                for gene in population:
                    print(gene.fitness_score, self.formula.num_clauses)
                    if gene.fitness_score == self.formula.num_clauses:
                        self.solution = gene.genotype
                        return True
                #population.sort(key=lambda x: x.fitness_score)
                #elite = population[-(self.POP_SIZE*self.ELITISM_RATE):]
                #others = population[:-(self.POP_SIZE*self.ELITISM_RATE)]
                #chosen = elite + self.selection(others)
                new_population = []
                for _ in range(self.POP_SIZE):
                    parents_gene = self.select(population)
                    new_gene = self.reproduce(parents_gene)
                    new_population.append(new_gene)
                population = new_population

    def fitness(self, genotype):
        score = 0
        #print("NEW GENOTYPE", genotype)
        for clause in self.formula.clauses:
            length = len(clause)
            for literal in clause:
                if literal == genotype[abs(literal) - 1]:
                    break
                else:
                    length -= 1
            if length > 0:
                score += 1
            # else:
            #    print(clause, genotype)
        #print("SCORE: ", score)
        return score

    def create_random_population(self):
        population = []
        for _ in range(self.POP_SIZE):
            genotype = self.get_random_genotype()
            population.append(Gene(genotype, self.fitness(genotype)))
        return population

    def get_random_genotype(self):
        return [i if randint(0, 1) else -i for i in range(1, self.formula.num_vars + 1)]

    def roulette_wheel(self, population):
        total = sum([gene.fitness_score for gene in population])
        cum_weights = [(gene.fitness_score / total)
                       * 10 for gene in population]
        return choices(population, cum_weights=cum_weights, k=2)

    def mating_pool(self, population):
        return self.roulette_wheel(population)
        # De més petit a més gran
        #population.sort(key=lambda x: x.fitness_score)

    def select(self, population):
        chosen = self.mating_pool(population)
        return chosen

    def reproduce(self, parents_gene):
        crossover_genotype = self.gene_concat(parents_gene)
        muted_genotype = self.mutate(crossover_genotype)
        return Gene(muted_genotype, self.fitness(muted_genotype))

    def mutate(self, genotype):
        new_genotype = copy(genotype)
        for i in range(len(genotype)):
            if random() < 0.05:
                genotype[i] *= -1
        return new_genotype

    def gene_concat(self, parents_gene):
        return parents_gene[0].genotype[:self.formula.num_vars//2] + parents_gene[1].genotype[self.formula.num_vars//2:]

        #Selection and reproduction repeted N times until new population. For each population, test if they satisfy

    def print_output(self):
        sys.stdout.write("c %s\n" % sys.argv[0][:-3])
        if self.solution:
            sys.stdout.write("s SATISFIABLE\n")
            sys.stdout.write("v %s\n" % " ".join(
                [str(cl) for cl in self.solution]))
        else:
            sys.stdout.write("s IDK\n")


class Gene():
    def __init__(self, genotype, fitness_score):
        self.genotype = genotype  # [1,-2,3,4,-5,6,7,-8]
        self.fitness_score = fitness_score  # 9

    def __repr__(self):
        return "(%s, %s)" % (self.genotype, self.fitness_score)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Incorrect number of arguments. Given %s. Expected 2.\n" %
                         len(sys.argv))
        sys.exit("Use: %s CNF_file" % sys.argv[0])
    cnf_path = sys.argv[1]
    if not os.path.isfile(cnf_path):
        sys.exit("ERROR: CNF file %s does not exist." % cnf_path)
    # "./benchmarks/10_20_3__1.cnf"
    solver = GASAT(1000, CNF(cnf_path))
    solver.solve()
    solver.print_output()


    #TODO: Problema: se queda en local-maxima, buscar manera per a que no passi aixo (random walk o potenciar les mutacions)
    #TODO: Canviar el select i el reproduce
    #TODO: Mirar el paper.
