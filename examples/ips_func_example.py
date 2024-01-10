from os import cpu_count
from typing import List

# algorithm module imports
from algorithm.impl import Elitism
from algorithm.module.mutation import Doer
from algorithm.module.crossover import TwoPoint
from algorithm.module.selection import Roulette

# function module imports
from function.impl import InversePolynomialSets
from function.module.measure import Propagations

# satprob lib imports
from lib_satprob.encoding import CNF
from lib_satprob.variables import Range
from lib_satprob.solver import Py2SatSolver
from lib_satprob.problem import SatProblem

# space module imports
from space.impl import BackdoorSet

# core module imports
from core.impl import Optimize
from core.model.point import Point
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

# other imports
from util.work_path import WorkPath
from output.impl import OptimizeLogger
from executor.impl import ProcessExecutor


def run_a5_1_search() -> List[Point]:
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

    function = InversePolynomialSets(
        measure=Propagations(),
    )
    sampling = Const(
        size=1024, split_into=256
    )

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('a5_1_64.cnf')

    problem = SatProblem(
        encoding=CNF(from_file=cnf_file),
        solver=Py2SatSolver(sat_name='g3'),
        input_set=Range(start=1, length=64),
        output_set=Range(start=14375, length=64)
    )  # read from file './examples/data/a5_1_64.cnf

    space = BackdoorSet(
        variables=Range(start=1, length=64)
    )  # for search space of 64 “on” vars

    workers = min(cpu_count(), 16)
    executor = ProcessExecutor(
        max_workers=workers
    )
    print(f'Running on {workers} threads')

    # log process to dir './examples/logs/<date_date>
    logs_path = root_path.to_path('logs', 'a5_1')
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
    'run_a5_1_search'
]
