import argparse
import sys

from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem
from lib_satprob.encoding import CNF, WCNF

from utility.work_path import WorkPath
from pipeline.rho_solve import solve

from function.module.measure import measures


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-f', '--formula', required=True)
    parser_.add_argument('-s', '--solvername', nargs='?', type=str, default='g3',
                         help='Solver name: g3, cd, cd15, etc (see PySAT Solvers list).')
    parser_.add_argument('-nr', '--nofearuns', nargs='?', type=int, default=40,
                         help='Number of runs of evolutionary algorithm for finding rho-backdoors.')
    parser_.add_argument('-seed', '--seedinitea', nargs='?', type=int, default=123,
                         help='Initialization seed for evolutionary algorithm.')
    parser_.add_argument('-np', '--nofprocesses', nargs='?', type=int, default=4,
                         help='Number of processes.')
    parser_.add_argument('-bds', '--backdoorsize', nargs='?', type=int, default=10,
                         help='Size of a single rho-backdoor.')
    parser_.add_argument('-tl', '--timelimit', nargs='?', type=int, default=0,
                         help='Set limit in seconds to solve one hard task. Use this option OR conflicts limit.')
    parser_.add_argument('-cl', '--conflictlimit', nargs='?', type=int, default=20000,
                         help='Set limit in conflicts to solve one hard task. Use this option OR time limit.')
    return parser_


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    formula_file = namespace.formula
    solver_name = namespace.solvername
    nof_ea_runs = namespace.nofearuns
    seed = namespace.seedinitea
    workers = namespace.nofprocesses
    bds = namespace.backdoorsize
    lim = max(namespace.timelimit, namespace.conflictlimit)
    limtype = 'conflicts' if namespace.conflictlimit > namespace.timelimit else 'time'
    measure = measures.get(f'measure:{limtype}')()

    data_path = WorkPath('examples', 'data')
    # enc_file = data_path.to_file('sgen_150.cnf')
    # cnf_file = data_path.to_file('pvs_4_7.cnf')

    solver = PySatSolver(sat_name=solver_name)
    # TODO надо чекать расширение файла (или читать хэдер) и если это wcnf то работать с wcnf
    encoding = CNF(from_file=formula_file)
    problem = SatProblem(
        solver, encoding
    )
    report = solve(problem=problem,
                   runs=nof_ea_runs,
                   measure=measure,
                   seed_offset=seed,
                   max_workers=workers,
                   bd_size=bds,
                   limit=lim)

