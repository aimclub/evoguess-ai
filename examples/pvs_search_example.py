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

# executor module imports
from executor.impl import ProcessExecutor

# core submodule imports
from core.module.sampling import Const
from core.module.limitation import WallTime

# other imports
from core.impl import Optimize
from util.work_path import WorkPath
from output.impl import OptimizeLogger
from core.module.comparator import MinValueMaxSize

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
    logs_path = root_path.to_path('logs', 'pvs_4_7')

    problem = SatProblem(
        encoding=CNF(from_file=cnf_file),
        solver=PySatSolver(sat_name='g3'),
    )
    solution = Optimize(
        problem=problem,
        space=BackdoorSet(
            by_vector=[],
            variables=rho_subset(
                problem,
                Range(start=1, length=1213),
                of_size=200
            )
        ),
        executor=ProcessExecutor(max_workers=16),
        sampling=Const(size=8192, split_into=2048),
        function=RhoFunction(
            penalty_power=2 ** 20,
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
        limitation=WallTime(from_string='02:00:00'),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
    ).launch()
