from core.impl import Optimize
from core.module.space import SearchSet
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

from output.impl import OptimizeLogger
from executor.impl import MPIExecutor

from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Interval

from function.impl import GuessAndDetermine
from function.module.measure import SolvingTime
from function.module.solver.impl.pysat import Glucose3

from algorithm.impl import Elitism
from algorithm.module.mutation import Doer
from algorithm.module.crossover import TwoPoint
from algorithm.module.selection import Roulette

from typings.work_path import WorkPath

if __name__ == '__main__':
    data_path = WorkPath('examples', 'data')
    logs_path = WorkPath('examples', 'logs')

    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=150)
        ),
        executor=MPIExecutor(),
        sampling=Const(size=4096, split_into=256),
        instance=Instance(
            encoding=CNF(from_file=data_path.to_file('sgen_150.cnf'))
        ),
        function=GuessAndDetermine(
            solver=Glucose3(),
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
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='00:20:00')
    ).launch()

    for point in solution:
        print(point)
