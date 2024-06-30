import os
import sys
import argparse

from pipeline.rho_solve_im import solve

from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem
from lib_satprob.problem import MaxSatProblem
from lib_satprob.encoding import CNF, WCNF

from function.module.budget import TaskBudget
from function.module.measure import Conflicts, SolvingTime


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('formula', type=str, help='File with input formula.')
    parser.add_argument('-s', '--solvername', nargs='?', type=str, default='cd195',
                        help='Solver name: cd195, g3, mcb, m22, etc (see PySAT Solvers list).')
    parser.add_argument('-nl', '--nofealimit', nargs='?', type=int, default=500,
                        help='Number of found rho-backdoors after which the algorithm will stop searching.')
    parser.add_argument('-ng', '--nofeagroups', nargs='?', type=int, default=4,
                        help='Number of groups with different rho value that can exist simultaneously.')
    parser.add_argument('-np', '--nofprocesses', nargs='?', type=int, default=12,
                        help='Number of simultaneously running islands in model.')
    parser.add_argument('-bds', '--backdoorsize', nargs='?', type=int, default=10,
                        help='Size of a single rho-backdoor that evolutionary algorithms will find.')
    parser.add_argument('-tl', '--timelimit', nargs='?', type=int, default=None,
                        help='Set limit in seconds to solve one hard task. Use this option OR conflicts limit.')
    parser.add_argument('-cl', '--conflictlimit', nargs='?', type=int, default=None,
                        help='Set limit in conflicts to solve one hard task. Use this option OR time limit.')
    parser.add_argument('-rs', '--randomseed', nargs='?', type=int, default=1234,
                        help='Random seed which is used to search for rho-backdoors')
    return parser


def get_encoding(filepath: str):
    if not os.path.isfile(filepath):
        raise Exception(f'File {filepath} is not exist.')

    if filepath.endswith('.cnf'):
        return CNF(from_file=filepath)
    elif filepath.endswith('.wcnf'):
        return WCNF(from_file=filepath)
    else:
        with open(filepath) as f:
            header = f.readline()

        if 'p cnf' in header:
            return CNF(from_file=filepath)
        elif 'p wcnf' in header:
            return WCNF(from_file=filepath)
        else:
            print('Wrong file extension:', filepath)
            print('Only CNF or WCNF encodings supported.')
            raise Exception('Wrong file extension.')


if __name__ == '__main__':
    args = get_parser().parse_args(
        sys.argv[1:]
    )

    encoding = get_encoding(args.formula)
    solver = PySatSolver(sat_name=args.solvername)

    problem = SatProblem(solver, encoding) \
        if encoding.slug == 'encoding:cnf' \
        else MaxSatProblem(solver, encoding)

    if args.timelimit is not None:
        limit = args.timelimit
        measure = SolvingTime()
    else:
        limit = args.conflictlimit
        limit = limit or 20000
        measure = Conflicts()

    budget = TaskBudget(limit)

    report = solve(
        budget=budget,
        problem=problem,
        measure=measure,
        bd_count=args.nofealimit,
        bd_size=args.backdoorsize,
        random_seed=args.randomseed,
        group_count=args.nofeagroups,
        max_workers=args.nofprocesses,
    )
