from os import cpu_count

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
from lib_satprob.problem import SatProblem
from lib_satprob.solver import Py2SatSolver

# core submodule imports
from core.impl import Optimize
from core.model.point import Point
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

# other imports
from space.impl import BackdoorSet
from util.work_path import WorkPath
from output.impl import OptimizeLogger
from executor.impl import ProcessExecutor


def run_bivium_search() -> Point:
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')

    logs_path = root_path.to_path('logs', 'bivium')
    cnf_file = data_path.to_file('bivium_200.cnf')
    problem = SatProblem(
        encoding=CNF(from_file=cnf_file),
        solver=Py2SatSolver(sat_name='g3'),
        input_set=Range(start=1, length=177),
        output_set=Range(start=1838, length=200),
    )

    workers = min(cpu_count(), 16)
    executor = ProcessExecutor(
        max_workers=workers
    )
    print(f'Running on {workers} threads')

    return Optimize(
        problem=problem,
        executor=executor,
        space=BackdoorSet(
            variables=Range(length=177)
        ),
        sampling=Const(
            size=8192,
            split_into=2048
        ),
        function=InversePolynomialSets(
            measure=Propagations(),
        ),
        algorithm=Elitism(
            elites_count=2,
            population_size=6,
            mutation=Doer(),
            crossover=TwoPoint(),
            selection=Roulette(),
            min_update_size=6
        ),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='12:00:00'),
    ).launch()[0]
