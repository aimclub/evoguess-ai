from algorithm.impl import LogSearch
from algorithm.module.mutation import LogDiv
from algorithm.module.selection import Roulette

from lib_satprob.encoding import CNF
from lib_satprob.variables import Range
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem

from function.impl import GuessAndDetermine
from function.module.measure import SolvingTime

from space.impl import BackdoorSet
from output.impl import OptimizeLogger
from executor.impl import ProcessExecutor

from core.impl import Optimize
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

from util.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    logs_path = root_path.to_path('logs')
    solver_path = root_path.to_path('solvers')

    cnf_file = data_path.to_file('pvs_4_7.cnf')
    solver_file = solver_path.to_file('kissat', 'kissat-rel-3.0.0', 'build')
    solution = Optimize(
        space=BackdoorSet(
            variables=Range(start=1, length=28)
        ),
        executor=ProcessExecutor(max_workers=4),
        sampling=Const(size=128, split_into=32),
        problem=SatProblem(
            solver=PySatSolver(),
            encoding=CNF(from_file=cnf_file),
        ),
        function=GuessAndDetermine(
            measure=SolvingTime(),
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
        limitation=WallTime(from_string='00:10:00'),
        logger=OptimizeLogger(logs_path.to_path('test47')),
    ).launch()

    for point in solution:
        print(point)
