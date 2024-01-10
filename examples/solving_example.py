# satprob lib imports
from lib_satprob.encoding import WCNF
from lib_satprob.problem import MaxSatProblem
from lib_satprob.solver import Report, PySatSolver

# other imports
from core.impl import Solving
from output.impl import NoneLogger
from util.work_path import WorkPath
from space.model import load_backdoors


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

    return Solving(
        problem=problem,
        logger=NoneLogger(),
    ).launch(*backdoors)
