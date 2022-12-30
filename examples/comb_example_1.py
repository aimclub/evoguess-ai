# function submodule imports
from function.module.solver import pysat
from function.module.measure import SolvingTime

# instance module imports
from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Indexes, make_backdoor

# other imports
from core.impl import Combine
from output.impl import OptimizeLogger
from typings.work_path import WorkPath
from executor.impl import ProcessExecutor

if __name__ == '__main__':
    str_backdoors = [
        '131 132 133 134 135',
        '22 24 25 32 33 34 35',
        '16 17 18 19 20 43 45',
        '43 44 45 81 82 83 84 85',
        '6 7 10 136 137 138 139 140',
    ]
    backdoors = [
        make_backdoor(Indexes(from_string=str_vars))
        for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('sgen_150.cnf')
    logs_path = root_path.to_path('logs', 'sgen_150')
    combine = Combine(
        instance=Instance(
            encoding=CNF(from_file=cnf_file)
        ),
        measure=SolvingTime(),
        solver=pysat.Glucose3(),
        logger=OptimizeLogger(logs_path),
        executor=ProcessExecutor(max_workers=4)
    )

    estimation = combine.launch(*backdoors)
    print(estimation)
