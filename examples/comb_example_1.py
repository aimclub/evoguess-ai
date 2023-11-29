# satprob lib imports
from lib_satprob.encoding import CNF
from lib_satprob.variables import Indexes
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem

# other imports
from core.impl import Combine
from space.model import Backdoor
from output.impl import OptimizeLogger
from executor.impl import ProcessExecutor

from util.work_path import WorkPath

if __name__ == '__main__':
    str_backdoors = [
        '131 132 133 134 135',
        '22 24 25 32 33 34 35',
        '16 17 18 19 20 43 45',
        '43 44 45 81 82 83 84 85',
        '6 7 10 136 137 138 139 140',
    ]
    backdoors = [
        Backdoor(variables=Indexes(
            from_string=str_vars
        )) for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('sgen_150.cnf')
    logs_path = root_path.to_path('logs', 'sgen_150_comb')
    estimation = Combine(
        problem=SatProblem(
            solver=PySatSolver(sat_name='g3'),
            encoding=CNF(from_file=cnf_file)
        ),
        logger=OptimizeLogger(logs_path),
        executor=ProcessExecutor(max_workers=4)
    ).launch(*backdoors)

    print(estimation)
