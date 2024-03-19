from os import cpu_count
from typing import List

# algorithm module imports
from algorithm.impl import Elitism
from algorithm.module.mutation import Doer
from algorithm.module.crossover import TwoPoint
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


def run_pvs_4_7_search() -> List[Point]:
    algorithm = Elitism(
        elites_count=2,
        population_size=6,
        mutation=Doer(),
        crossover=TwoPoint(),
        selection=Roulette(),
        min_update_size=6
    )
    limitation = WallTime(
        from_string='04:00:00'
    )

    function = RhoFunction(
        penalty_power=2 ** 20,
        measure=Propagations(),
    )
    sampling = Const(
        size=1024, split_into=256
    )

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('pvs_4_7.cnf')

    problem = SatProblem(
        encoding=CNF(from_file=cnf_file),
        solver=PySatSolver(sat_name='g3'),
    )  # read from file './examples/data/sort/pvs_4_7.cnf

    space = BackdoorSet(
        by_vector=[],
        variables=rho_subset(
            problem,
            Range(length=1213),
            of_size=100
        )
    )  # reduce to subset of 100 “off” var

    workers = min(cpu_count(), 16)
    executor = ProcessExecutor(
        max_workers=workers
    )
    print(f'Running on {workers} threads')

    # log process to dir './examples/logs/<date_date>
    logs_path = root_path.to_path('logs', 'pvs_4_7')
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
    'run_pvs_4_7_search'
]
