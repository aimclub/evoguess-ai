from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem
from lib_satprob.encoding import CNF, WCNF

from utility.work_path import WorkPath
from pipeline.rho_solve import solve

if __name__ == '__main__':
    data_path = WorkPath('examples', 'data')
    # enc_file = data_path.to_file('sgen_150.cnf')
    cnf_file = data_path.to_file('pvs_4_7.cnf')

    solver = PySatSolver(sat_name='g3')
    encoding = CNF(from_file=cnf_file)
    problem = SatProblem(
        solver, encoding
    )
    report = solve(problem, 40, 123)
