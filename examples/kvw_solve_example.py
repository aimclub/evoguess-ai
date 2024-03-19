from os import cpu_count

# function submodule imports
from function.module.budget import TaskBudget
from function.module.measure import Conflicts

# satprob lib imports
from lib_satprob.encoding import WCNF
from lib_satprob.problem import MaxSatProblem
from lib_satprob.solver import Report, PySatSolver

# other imports
from core.impl import CombineT
from output.impl import NoneLogger
from utility.work_path import WorkPath
from space.model import load_backdoors


def run_kvw_solve() -> Report:
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')

    bds_file = data_path.to_file('lec_kvw_12.bds')
    backdoors = load_backdoors(from_file=bds_file)

    wcnf_file = data_path.to_file('lec_kvw_12.wcnf')
    problem = MaxSatProblem(
        encoding=WCNF(from_file=wcnf_file),
        solver=PySatSolver(max_sat_alg='rc2')
    )

    workers = min(cpu_count(), 16)
    print(f'Running on {workers} threads')

    return CombineT(
        problem=problem,
        measure=Conflicts(),
        logger=NoneLogger(),
        max_workers=workers,
        budget=TaskBudget(value=20000),
    ).launch(*backdoors)


__all__ = [
    'run_kvw_solve'
]
