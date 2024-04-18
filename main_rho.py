import argparse
import sys
import os

from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem
from lib_satprob.problem import MaxSatProblem
from lib_satprob.encoding import CNF, WCNF


from utility.work_path import WorkPath
from pipeline.rho_solve import solve

from function.module.measure import measures


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('formula', type=str, help='File with input formula.')
    parser_.add_argument('-s', '--solvername', nargs='?', type=str, default='Cadical195',
                         help='Solver name: cd195, g3, mcb, m22, etc (see PySAT Solvers list).')
    parser_.add_argument('-nr', '--nofearuns', nargs='?', type=int, default=40,
                         help='Number of runs of evolutionary algorithm for finding rho-backdoors.')
    parser_.add_argument('-np', '--nofprocesses', nargs='?', type=int, default=4,
                         help='Number of processes.')
    parser_.add_argument('-bds', '--backdoorsize', nargs='?', type=int, default=10,
                         help='Size of a single rho-backdoor.')
    parser_.add_argument('-tl', '--timelimit', nargs='?', type=int, default=0,
                         help='Set limit in seconds to solve one hard task. Use this option OR conflicts limit.')
    parser_.add_argument('-cl', '--conflictlimit', nargs='?', type=int, default=0,
                         help='Set limit in conflicts to solve one hard task. Use this option OR time limit.')
    return parser_


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    formula_file = namespace.formula
    solver_name = namespace.solvername
    nof_ea_runs = namespace.nofearuns
    workers = namespace.nofprocesses
    bds = namespace.backdoorsize
    timelim = namespace.timelimit
    conflictlim = namespace.conflictlimit
    if timelim == 0 and conflictlim == 0:
        conflictlim = 20000
    lim = max(timelim, conflictlim)
    limtype = 'conflicts' if conflictlim > timelim else 'time'
    measure = measures.get(f'measure:{limtype}')()

    data_path = WorkPath('examples', 'data')
    # enc_file = data_path.to_file('sgen_150.cnf')
    # cnf_file = data_path.to_file('pvs_4_7.cnf')

    solver = PySatSolver(sat_name=solver_name)
    # problem = encode_problem(formula_file, solver)
    if not os.path.isfile(formula_file):
        raise Exception(f'File {formula_file} is not exist.')
    if formula_file.endswith('.cnf'):
        encoding = CNF(from_file=formula_file)
        problem = SatProblem(
            solver, encoding
        )
    elif formula_file.endswith('.wcnf'):
        encoding = WCNF(from_file=formula_file)
        problem = MaxSatProblem(
            solver, encoding
        )
    else:
        with open(formula_file) as f:
            header = f.readline()
        if 'p cnf' in header:
            encoding = CNF(from_file=formula_file)
            problem = SatProblem(
                solver, encoding
            )
        elif 'p wcnf' in header:
            encoding = WCNF(from_file=formula_file)
            problem = MaxSatProblem(
                solver, encoding
            )
        else:
            print('Wrong file extension:', formula_file)
            print('CNF or WCNF files supported.')
            raise Exception('Wrong file extension.')
    report = solve(problem=problem,
                   runs=nof_ea_runs,
                   measure=measure,
                   seed_offset=123,
                   max_workers=workers,
                   bd_size=bds,
                   limit=lim,
                   log_path=None,
                   iter_count=3000)



