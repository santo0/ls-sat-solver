class CNF:
    def __init__(self, cnf_path):
        self.name = ""
        self.clauses = []
        self.num_vars = -1
        self.num_clauses = -1
        self._get_cnf(cnf_path)

    def _get_cnf(self, cnf_path):
        with open(cnf_path) as f:
            self.name = f.readline().strip()
            conf_line = f.readline().strip().split()
            self.num_vars = int(conf_line[2])
            self.num_clauses = int(conf_line[3])
            #p cnf 10 20
            #p cnf numvars, numclauses
            clause_line = f.readline().strip().split()
            while clause_line:
                self.clauses.append(clause_line[:-1])
                clause_line = f.readline().strip().split()
    
    def __str__(self):
        return "name: %s, num_vars: %i, num_clauses: %i" % (self.name, self.num_vars, self.num_clauses) 
    



if __name__ == "__main__":
    print("CNF representation")
    cnf_path = "./benchmarks/10_20_3__1.cnf"
    cnf = CNF(cnf_path)
    print(cnf)
    print(cnf.clauses)