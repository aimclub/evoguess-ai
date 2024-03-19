from os import cpu_count
from itertools import combinations

# lib_satprob module imports
from lib_satprob.encoding import CNF
from lib_satprob.problem import SatProblem
from lib_satprob.solver import PySatSolver
from lib_satprob.variables import Indexes

# other imports
from core.impl import Combine
from space.model import Backdoor
from output.impl import NoneLogger
from executor.impl import ProcessExecutor

from utility.work_path import WorkPath


def run_pvs_quality():
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('pvs_4_7.cnf')

    problem = SatProblem(
        solver=PySatSolver(sat_name='g3'),
        encoding=CNF(from_file=cnf_file)
    )

    workers = min(cpu_count(), 16)
    executor = ProcessExecutor(
        max_workers=workers
    )
    print(f'Running on {workers} threads')

    combine = Combine(
        problem=problem,
        executor=executor,
        logger=NoneLogger(),
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

    for count in range(6, 7):
        for combination in combinations(str_backdoors, count):
            backdoors = [
                Backdoor(variables=Indexes(
                    from_string=str_vars
                )) for str_vars in str_backdoors
            ]
            _, stats, _, _ = combine.launch(*backdoors)
            print(stats['time'] / full_time, combination)


__all__ = [
    'run_pvs_quality'
]
