from os import cpu_count
from typing import List

# algorithm module imports
from algorithm.impl import MuPlusLambda
from algorithm.module.mutation import FixSize
from algorithm.module.selection import Roulette

# function module imports
from function.impl import RhoFunction
from function.module.measure import Propagations

# satprob lib imports
from lib_satprob.encoding import WCNF
from lib_satprob.variables import Range
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import MaxSatProblem

# space module imports
from space.impl import BackdoorSet

# executor module imports
from executor.impl import ThreadExecutor

# core module imports
from core.impl import Optimize
from core.model.point import Point
from core.module.sampling import Const
from core.module.limitation import Iteration
from core.module.comparator import MinValueMaxSize

# other imports
from output.impl import NoneLogger
from util.work_path import WorkPath


def run_jss_search(count=500) -> List[Point]:
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    wcnf_file = data_path.to_file('jss_hard.wcnf')

    problem = MaxSatProblem(
        encoding=WCNF(from_file=wcnf_file),
        solver=PySatSolver(sat_name='g3'),
    )

    workers = min(cpu_count(), 16)
    executor = ThreadExecutor(
        max_workers=workers
    )
    print(f'Running on {workers} threads')

    split_into = 1024 // workers
    size = split_into * workers

    points = []
    for i in range(count):
        point = Optimize(
            problem=problem,
            executor=executor,
            space=BackdoorSet(
                by_vector=[],
                variables=Range(
                    length=9950717
                ),
            ),
            sampling=Const(
                size=size,
                split_into=split_into
            ),
            logger=NoneLogger(),
            function=RhoFunction(
                penalty_power=2 ** 20,
                measure=Propagations(),
            ),
            algorithm=MuPlusLambda(
                mu_size=1,
                lambda_size=1,
                mutation=FixSize(10),
                selection=Roulette(),
            ),
            limitation=Iteration(value=3000),
            comparator=MinValueMaxSize(),
        ).launch()[0]
        points.append(point)

        print(
            f'{i + 1:3d}/{count} ',
            point.searchable,
            point.get('rho_value')
        )

    return points


__all__ = [
    'run_jss_search'
]
