import subprocess
import sys
import re
regexp = re.compile(r'^SATISFIABLE')


# peak 4.25
NUM_VARS_STEP = 3
NUM_VARS_LIMIT = 200
CLAUSE_LEN = 3
RATIO = 4.25


def main():
    for num_vars in range(NUM_VARS_STEP, NUM_VARS_LIMIT, NUM_VARS_STEP):
        sat_found = False   
        while not sat_found:
            exec_gen_cnf = subprocess.run(['python',  'rnd-cnf-gen.py', str(num_vars), str(
                int(num_vars*RATIO)), str(CLAUSE_LEN)], stdout=subprocess.PIPE)
            gen_cnf = exec_gen_cnf.stdout.decode('utf-8')

            file_name = "%s-%s-%s" % (str(num_vars),
                                      str(int(num_vars*RATIO)), str(CLAUSE_LEN))
            with open('./tmp/%s.cnf' % file_name, 'w') as f:
                f.write(gen_cnf)

            exec_minisat = subprocess.run(
                ['./minisat', './tmp/%s.cnf' % file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out_minisat = exec_minisat.stdout.decode('utf-8')
            if regexp.search(out_minisat):
                sat_found = True
                subprocess.run(['mv', './tmp/%s.cnf' % file_name,
                                './benchmarks/sat_cnf/%s.cnf' % file_name], stdout=subprocess.PIPE)
                print("Created ./benchmarks/sat_cnf/%s.cnf"% file_name)
            else:
                subprocess.run(['mv', './tmp/%s.cnf' % file_name,
                                './benchmarks/unsat_cnf/%s.cnf' % file_name], stdout=subprocess.PIPE)
                print("Created ./benchmarks/unsat_cnf/%s.cnf"% file_name)


if __name__ == '__main__':
    main()
