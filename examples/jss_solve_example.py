# satprob lib imports
from lib_satprob.encoding import WCNF
from lib_satprob.problem import SatProblem
from lib_satprob.solver import Report, Kissat

# other imports
from core.impl import Solving
from output.impl import NoneLogger
from utility.work_path import WorkPath
from space.model import load_backdoors


def run_jss_solve() -> Report:
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    solvers_path = root_path.to_path('solvers')

    bds_file = data_path.to_file('jss_hard.bds')
    backdoors = load_backdoors(from_file=bds_file)

    exec_file = solvers_path.to_file('kissat', 'kissat')
    wcnf_file = data_path.to_file('jss_hard.wcnf')
    problem = SatProblem(
        encoding=WCNF(from_file=wcnf_file).from_hard(),
        solver=Kissat(from_executable=exec_file)
    )

    return Solving(
        problem=problem,
        logger=NoneLogger(),
    ).launch(*backdoors)


__all__ = [
    'run_jss_solve'
]
