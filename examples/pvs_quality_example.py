from itertools import combinations

# lib_satprob module imports
from lib_satprob.encoding import CNF
from lib_satprob.problem import SatProblem
from lib_satprob.solver import PySatSolver
from lib_satprob.variables import Indexes

# other imports
from core.impl import Combine
from space.model import Backdoor
from output.impl import OptimizeLogger
from executor.impl import ProcessExecutor
from function.module.measure import SolvingTime

from util.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples', root='..')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')

    measure = SolvingTime()
    problem = SatProblem(
        solver=PySatSolver(sat_name='g3'),
        encoding=CNF(from_file=cnf_file)
    )

    logs_path = root_path.to_path('logs', 'pvs_4_7_s')
    combine = Combine(
        problem=problem,
        logger=OptimizeLogger(logs_path),
        executor=ProcessExecutor(max_workers=16)
    )

    full_time = problem.solve().stats['time']

    str_backdoors = [
        '348 470 682 684 686 687 702 706 708 710 715',
        '164 176 177 348 470 648 651 683 684 688 689',
        '118 155 164 176 177 204 230 348 470 684 1188',
        '348 470 682 683 684 686 687 688 689 694 698',
        '164 176 177 348 470 683 684 689 708 710 715',
        '174 438 470 536 537 546 549 551 634 635 1046 1047',
    ]

    with combine.logger as handle:
        for count in range(6, 7):
            for combination in combinations(str_backdoors, count):
                backdoors = [
                    Backdoor(variables=Indexes(
                        from_string=str_vars
                    )) for str_vars in str_backdoors
                ]
                estimation = combine.launch(*backdoors)
                handle._format({
                    'estimation': estimation,
                    'combination': combination,
                }, filename='log.jsonl')

                print(estimation['value'] / full_time, combination)
