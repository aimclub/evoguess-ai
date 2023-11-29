from core.impl import Optimize
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

from space.impl import BackdoorSet
from output.impl import OptimizeLogger
from executor.impl import MPIExecutor

from lib_satprob.encoding import CNF
from lib_satprob.variables import Range
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem

from function.impl import GuessAndDetermine
from function.module.budget import AutoBudget
from function.module.measure import SolvingTime

from algorithm.impl import Elitism
from algorithm.module.mutation import Doer
from algorithm.module.crossover import TwoPoint
from algorithm.module.selection import Roulette

from util.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('sgen_150.cnf')
    log_path = root_path.to_path('logs', 'sgen150')

    solution = Optimize(
        space=BackdoorSet(
            by_vector=[],
            variables=Range(start=1, length=150)
        ),
        executor=MPIExecutor(),
        sampling=Const(size=4096, split_into=256),
        problem=SatProblem(
            encoding=CNF(from_file=cnf_file),
            solver=PySatSolver(sat_name='g3'),
        ),
        function=GuessAndDetermine(
            budget=AutoBudget(),
            measure=SolvingTime()
        ),
        algorithm=Elitism(
            elites_count=2,
            population_size=6,
            mutation=Doer(),
            crossover=TwoPoint(),
            selection=Roulette(),
        ),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(log_path),
        limitation=WallTime(from_string='00:20:00')
    ).launch()

    for point in solution:
        print(point)
