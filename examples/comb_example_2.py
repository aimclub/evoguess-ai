# satprob lib imports
from lib_satprob.encoding import CNF
from lib_satprob.problem import SatProblem
from lib_satprob.solver import PySatSolver
from lib_satprob.variables import Indexes

# other imports
from core.impl import Combine
from space.model import Backdoor
from output.impl import OptimizeLogger
from executor.impl import ProcessExecutor

from util.work_path import WorkPath

if __name__ == '__main__':
    str_backdoors = [
        '348 470 682 684 686 687 702 706 708 710 715',
        '164 176 177 348 470 648 651 683 684 688 689',
        '118 155 164 176 177 204 230 348 470 684 1188',
        '348 470 682 683 684 686 687 688 689 694 698',
        '164 176 177 348 470 683 684 689 708 710 715',
    ]
    backdoors = [
        Backdoor(variables=Indexes(
            from_string=str_vars
        )) for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
    logs_path = root_path.to_path('logs', 'pvs_4_7_comb')
    estimation = Combine(
        problem=SatProblem(
            solver=PySatSolver(sat_name='g3'),
            encoding=CNF(from_file=cnf_file)
        ),
        logger=OptimizeLogger(logs_path),
        executor=ProcessExecutor(max_workers=4)
    ).launch(*backdoors)

    print(estimation)
