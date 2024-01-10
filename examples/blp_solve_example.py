# satprob lib imports
from lib_satprob.encoding import WCNF
from lib_satprob.problem import MaxSatProblem
from lib_satprob.solver import Report, Loandra

# other imports
from core.impl import Solving
from output.impl import NoneLogger
from util.work_path import WorkPath
from space.model import load_backdoors


def run_blp_18_solve() -> Report:
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    solvers_path = root_path.to_path('solvers')

    bds_file = data_path.to_file('blp_k18_del300.bds')
    backdoors = load_backdoors(from_file=bds_file)

    exec_file = solvers_path.to_file('loandra', 'loandra')
    wcnf_file = data_path.to_file('blp_k18_del300.wcnf')
    problem = MaxSatProblem(
        encoding=WCNF(from_file=wcnf_file),
        solver=Loandra(from_executable=exec_file)
    )

    return Solving(
        problem=problem,
        logger=NoneLogger(),
    ).launch(*backdoors)
