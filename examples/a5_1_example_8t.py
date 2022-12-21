from core.impl import Optimize
from core.module.space import InputSet
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

from output.impl import OptimizeLogger
from executor.impl import ThreadExecutor

from instance.impl import StreamCipher
from instance.module.encoding import CNF
from instance.module.variables import Interval

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
        executor=ThreadExecutor(max_workers=8),
        sampling=Const(size=256, split_into=64),
        instance=StreamCipher(
            input_set=Interval(start=1, length=64),
            output_set=Interval(start=8298, length=128),
            encoding=CNF(from_file=data_path.to_file('a5_1.cnf'))
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
        limitation=WallTime(from_string='01:00:00')
    ).launch()

    for point in solution:
        print(point)
