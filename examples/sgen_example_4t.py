from core.impl import Optimize
from core.module.space import InputSet
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

from output.impl import OptimizeLogger
from executor.impl import ThreadExecutor

from instance.impl import Instance
from instance.module.encoding import CNF

from function.impl import GuessAndDetermine
from function.module.measure import SolvingTime
from function.module.solver.impl.pysat import Glucose3

from algorithm.impl import MuPlusLambda
from algorithm.module.mutation import Doer
from algorithm.module.selection import Roulette

from typings.work_path import WorkPath

if __name__ == '__main__':
    data_path = WorkPath('examples', 'data')
    logs_path = WorkPath('examples', 'logs')

    solution = Optimize(
        space=InputSet(),
        executor=ThreadExecutor(max_workers=4),
        sampling=Const(size=128, split_into=32),
        instance=Instance(
            encoding=CNF(from_file=data_path.to_file('sgen_150.cnf'))
        ),
        function=GuessAndDetermine(
            solver=Glucose3(),
            measure=SolvingTime()
        ),
        algorithm=MuPlusLambda(
            mu_size=1,
            lambda_size=1,
            mutation=Doer(),
            selection=Roulette()
        ),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='00:20:00')
    ).launch()

    for point in solution:
        print(point)
