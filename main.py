from algorithm.impl import LogSearch
from algorithm.module.mutation import LogDiv
from algorithm.module.selection import Roulette

from function.impl import GuessAndDetermine
from function.module.solver import Kissat
from function.module.budget import AutoBudget
from function.module.measure import SolvingTime

from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Range

from space.impl import IntervalSet

from util.work_path import WorkPath
from output.impl import OptimizeLogger
from executor.impl import ProcessExecutor

from core.impl import Optimize
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
    solver_path = root_path.to_path('solvers', 'kissat-rel-3.0.0')

    solver_file = solver_path.to_file('kissat', 'build')
    logs_path = root_path.to_path('logs', 'test47')
    solution = Optimize(
        space=IntervalSet(
            indexes=Range(start=1, length=850),
            by_vector=[0] * 213 + [1] * 1000
        ),
        executor=ProcessExecutor(max_workers=1),
        sampling=Const(size=4, split_into=1),
        instance=Instance(
            encoding=CNF(from_file=cnf_file),
        ),
        function=GuessAndDetermine(
            measure=SolvingTime(),
            budget=AutoBudget(),
            solver=Kissat(solver_file),
        ),
        algorithm=LogSearch(
            population_size=6,
            mutation=LogDiv(
                max_noise_scale=0.95
            ),
            selection=Roulette(),
            min_update_size=6
        ),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='00:30:00'),
    ).launch()

    for point in solution:
        print(point)
