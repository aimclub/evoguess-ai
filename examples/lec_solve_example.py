# function submodule imports
from function.module.budget import TaskBudget
from function.module.measure import Conflicts

# satprob lib imports
from lib_satprob.encoding import WCNF
from lib_satprob.variables import Indexes
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import MaxSatProblem

# other imports
from core.impl import CombineT
from space.model import Backdoor
from util.work_path import WorkPath
from output.impl import OptimizeLogger
from executor.impl import ProcessExecutor

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')

    bds_file = data_path.to_file('lec_cvk_11x11.bds')
    wcnf_file = data_path.to_file('lec_cvk_11x11.wcnf')
    log_path = root_path.to_path('logs', 'cvk_11x11_comb')

    with open(bds_file, 'r') as handle:
        backdoors = [
            Backdoor(variables=Indexes(
                from_string=line.strip()
            )) for line in handle.readlines()
        ]

    problem = MaxSatProblem(
        solver=PySatSolver(),
        encoding=WCNF(from_file=wcnf_file)
    )
    estimation = CombineT(
        problem=problem,
        measure=Conflicts(),
        budget=TaskBudget(value=5000),
        logger=OptimizeLogger(log_path),
        executor=ProcessExecutor(max_workers=16)
    ).launch(*backdoors)

    print(estimation)
