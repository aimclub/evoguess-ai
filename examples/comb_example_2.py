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
        '348 470 682 684 686 687 702 706 708 710 715',
        '164 176 177 348 470 648 651 683 684 688 689',
        '118 155 164 176 177 204 230 348 470 684 1188',
        '348 470 682 683 684 686 687 688 689 694 698',
        '164 176 177 348 470 683 684 689 708 710 715',
    ]
    backdoors = [
        make_backdoor(Indexes(from_string=str_vars))
        for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
    logs_path = root_path.to_path('logs', 'pvs_4_7')
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
