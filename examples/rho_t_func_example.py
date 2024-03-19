from os import cpu_count
from typing import List

# algorithm module imports
from algorithm.impl import MuPlusLambda
from algorithm.module.mutation import Doer
from algorithm.module.selection import Roulette

# function module imports
from function.impl import RhoTFunction
from function.module.budget import TaskBudget
from function.module.measure import Conflicts

# satprob lib imports
from lib_satprob.encoding import WCNF
from lib_satprob.variables import Range
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import MaxSatProblem

# space module imports
from space import rho_subset
from space.impl import BackdoorSet

# core module imports
from core.impl import Optimize
from core.model.point import Point
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

# other imports
from utility.work_path import WorkPath
from output.impl import OptimizeLogger
from executor.impl import ProcessExecutor


def run_cvk_11_search() -> List[Point]:
    algorithm = MuPlusLambda(
        mu_size=1,
        lambda_size=1,
        mutation=Doer(),
        selection=Roulette(),
    )
    limitation = WallTime(
        from_string='12:00:00'
    )

    function = RhoTFunction(
        measure=Conflicts(),
        penalty_power=2 ** 12,
        budget=TaskBudget(value=5000),
    )
    sampling = Const(
        size=1024, split_into=64
    )

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    wcnf_file = data_path.to_file('lec_cvk_11.wcnf')

    problem = MaxSatProblem(
        encoding=WCNF(from_file=wcnf_file),
        solver=PySatSolver(sat_name='g3'),
    )  # read from file './examples/data/lec_cvk_11.cnf

    space = BackdoorSet(
        by_vector=[],
        variables=rho_subset(
            problem,
            Range(length=5061),
            of_size=300
        )
    )  # reduce to subset of 300 “off” var

    workers = min(cpu_count(), 16)
    executor = ProcessExecutor(
        max_workers=workers
    )
    print(f'Running on {workers} threads')

    # log process to dir './examples/logs/<date_date>
    logs_path = root_path.to_path('logs', 'cvk_11')
    return Optimize(
        space=space,
        problem=problem,
        executor=executor,
        sampling=sampling,
        function=function,
        algorithm=algorithm,
        limitation=limitation,
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
    ).launch()


__all__ = [
    'run_cvk_11_search'
]
