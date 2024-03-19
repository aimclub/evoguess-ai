from os import cpu_count

# satprob lib imports
from lib_satprob.encoding import WCNF
from lib_satprob.problem import MaxSatProblem
from lib_satprob.solver import Report, PySatSolver

# function module imports
from function.module.budget import TaskBudget
from function.module.measure import Conflicts

# other imports
from core.impl import CombineT
from output.impl import NoneLogger
from utility.work_path import WorkPath
from space.model import load_backdoors
from executor.impl import ProcessExecutor


def run_cvk_11_solve() -> Report:
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')

    bds_file = data_path.to_file('lec_cvk_11.bds')
    backdoors = load_backdoors(from_file=bds_file)

    wcnf_file = data_path.to_file('lec_cvk_11.wcnf')
    problem = MaxSatProblem(
        encoding=WCNF(from_file=wcnf_file),
        solver=PySatSolver(sat_name='g3')
    )

    workers = min(cpu_count(), 16)
    print(f'Running on {workers} threads')

    return CombineT(
        problem=problem,
        measure=Conflicts(),
        logger=NoneLogger(),
        max_workers=workers,
        budget=TaskBudget(value=5000),
    ).launch(*backdoors)


__all__ = [
    'run_cvk_11_solve'
]
