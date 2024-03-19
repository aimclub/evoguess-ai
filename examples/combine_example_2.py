from os import cpu_count

# satprob lib imports
from lib_satprob.encoding import CNF
from lib_satprob.problem import SatProblem
from lib_satprob.solver import Report, PySatSolver

# other imports
from core.impl import Combine
from output.impl import NoneLogger
from utility.work_path import WorkPath
from space.model import load_backdoors
from executor.impl import ProcessExecutor


def run_pvs_4_7_solve() -> Report:
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')

    bds_file = data_path.to_file('pvs_4_7.bds')
    backdoors = load_backdoors(from_file=bds_file)

    cnf_file = data_path.to_file('pvs_4_7.cnf')
    problem = SatProblem(
        encoding=CNF(from_file=cnf_file),
        solver=PySatSolver(sat_name='g3')
    )

    workers = min(cpu_count(), 16)
    executor = ProcessExecutor(
        max_workers=workers
    )
    print(f'Running on {workers} threads')

    return Combine(
        problem=problem,
        executor=executor,
        logger=NoneLogger(),
    ).launch(*backdoors)


__all__ = [
    'run_pvs_4_7_solve'
]
