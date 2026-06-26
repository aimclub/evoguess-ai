from algorithm.module.selection import Roulette
from algorithm.module.mutation import Uniform
from function.module.budget import TaskBudget
from algorithm.impl import MuPlusLambda

from lib_satprob.problem import SatProblem
from lib_satprob.variables import Range
from lib_satprob.encoding import CNF
from lib_satprob.solver import Kissat

from function.module.measure import Conflicts
from function.impl import InverseBackdoorSets

from executor.impl import MPIExecutor
from output.impl import OptimizeLogger
from space.impl import BackdoorSet

from core.module.comparator import MinValueMaxSize
from core.module.limitation import WallTime
from core.module.sampling import Const
from core.impl import Optimize

from utility.work_path import WorkPath

if __name__ == '__main__':
    examples_path = WorkPath('examples')
    log_path = WorkPath('logs', 'a5_1_test')

    solvers_path = examples_path.to_path('solvers')
    solver_file = solvers_path.to_file('kissat')

    data_path = examples_path.to_path('data')
    cnf_file = data_path.to_file('a5_1_64.cnf')

    solution = Optimize(
        space=BackdoorSet(
            variables=Range(start=1, length=64),
            of_size=56,
        ),
        executor=MPIExecutor(),
        sampling=Const(size=128, split_into=32),
        problem=SatProblem(
            output_set=Range(from_string='14375..14438'),
            input_set=Range(start=1, length=64),
            encoding=CNF(from_file=cnf_file),
            solver=Kissat(solver_file),
        ),
        function=InverseBackdoorSets(
            budget=TaskBudget(10000),
            measure=Conflicts(),
        ),
        algorithm=MuPlusLambda(
            selection=Roulette(),
            mutation=Uniform(
                flip_scale=1.
            ),
            min_update_size=1,
            lambda_size=1,
            mu_size=1,
        ),
        comparator=MinValueMaxSize(),
        limitation=WallTime(from_string='00:10:00'),
        logger=OptimizeLogger(log_path),
    ).launch()

    for point in solution:
        print(point)
