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
from lib_satprob.encoding import CNF
from lib_satprob.variables import Range
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem

# space module imports
from space import rho_subset
from space.impl import BackdoorSet

# executor module imports
from executor.impl import ProcessExecutor

# core submodule imports
from core.impl import Optimize
from core.model.point import Point
from core.module.sampling import Const
from core.module.limitation import Iteration
from core.module.comparator import MinValueMaxSize

# other imports
from output.impl import NoneLogger
from utility.work_path import WorkPath


def run_pvs_4_7_search(count=6) -> List[Point]:
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')

    workers = min(cpu_count(), 16)
    executor = ProcessExecutor(
        max_workers=workers
    )
    print(f'Running on {workers} threads')

    split_into = 256 // workers
    size = split_into * workers

    cnf_file = data_path.to_file('pvs_4_7.cnf')
    problem = SatProblem(
        encoding=CNF(from_file=cnf_file),
        solver=PySatSolver(sat_name='g3'),
    )

    points = []
    for i in range(count):
        point = Optimize(
            problem=problem,
            executor=executor,
            space=BackdoorSet(
                by_vector=[],
                variables=rho_subset(
                    problem,
                    Range(length=1213),
                    of_size=300
                )
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
            comparator=MinValueMaxSize(),
            limitation=Iteration(value=1000)
        ).launch()[0]
        points.append(point)

        print(
            f'{i + 1:3d}/{count} ',
            point.searchable,
            point.get('rho_value')
        )

    return points
