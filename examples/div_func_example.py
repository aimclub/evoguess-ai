from os import cpu_count
from typing import List

# algorithm module imports
from algorithm.impl import MuPlusLambda
from algorithm.module.mutation import Doer
from algorithm.module.selection import Roulette

# function module imports
from function.impl import DivFunction
from function.module.measure import SolvingTime

# satprob lib imports
from lib_satprob.encoding import WCNF
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import MaxSatProblem

# space module imports
from space import init_partition

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
        selection=Roulette()
    )
    limitation = WallTime(
        from_string='04:00:00'
    )

    function = DivFunction(
        measure=SolvingTime(),
    )
    sampling = Const(
        size=64, split_into=16
    )

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    wcnf_file = data_path.to_file('blp_k18_del300.wcnf')

    problem, space = init_partition(
        weaken=2 ** 48,
        problem=MaxSatProblem(
            encoding=WCNF(from_file=wcnf_file),
            solver=PySatSolver(sat_name='g3'),
        )
    )

    workers = min(cpu_count(), 16)
    executor = ProcessExecutor(
        max_workers=workers
    )
    print(f'Running on {workers} threads')

    # log process to dir './examples/logs/<date_date>
    logs_path = root_path.to_path('logs', 'blp_k18_del300')
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
