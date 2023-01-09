import sys

from math import ceil
from typing import List, Dict, Any
from time import time as now
from itertools import chain, product

from output import Logger
from executor import Executor
from instance import Instance

from ..abc import Core

from instance.module.variables import Backdoor
from instance.module.variables.vars import compress, Assumptions

from function.module.measure import Measure
from function.models import Status, Estimation
from function.impl.function_gad import sequence_mapper
from function.module.solver import Solver, Report, IncrSolver

from typings.optional import Int
from util.iterable import concat, slice_by


def get_propagation(solver: IncrSolver, backdoor: Backdoor) -> Report:
    var_bases = backdoor.get_var_bases()
    time_sum, value_sum, up_tasks, hard_tasks = 0, 0, [], []
    for substitution in map(sequence_mapper(var_bases), range(backdoor.power())):
        values = {var: value for var, value in zip(backdoor, substitution)}
        assumptions, _ = compress(*(var.supplements(values) for var in backdoor))
        time, value, status, _ = solver.propagate(assumptions, add_model=False)
        (up_tasks if status == Status.RESOLVED else hard_tasks).append(assumptions)
        time_sum, value_sum = time_sum + time, value_sum + value

    status = Status.SOLVED if len(hard_tasks) else Status.RESOLVED
    return Report(time_sum, value_sum, status, (up_tasks, hard_tasks))


def hard_worker(solver: Solver, measure: Measure, instance: Instance,
                up_tasks: List[Assumptions], hard_tasks: List[Assumptions]) -> Report:
    time_sum, value_sum, encoding_data = 0, 0, instance.encoding.get_data()
    with solver.use_incremental(encoding_data, measure) as incremental:
        for up_task_assumptions in chain(up_tasks, hard_tasks):
            time, value, _, _ = incremental.solve(up_task_assumptions, add_model=False)
            time_sum, value_sum = time_sum + time, value_sum + value

    return Report(time_sum, value_sum, Status.RESOLVED, None)


class Combine(Core):
    slug = 'core:combine'

    def __init__(self,
                 logger: Logger,
                 solver: Solver,
                 measure: Measure,
                 instance: Instance,
                 executor: Executor,
                 random_seed: Int = None):
        self.solver = solver
        self.measure = measure
        self.executor = executor
        super().__init__(logger, instance, random_seed)

    def launch(self, *backdoors: Backdoor) -> Estimation:
        encoding_data = self.instance.encoding.get_data()
        total_var_set, start_stamp = set(concat(*backdoors)), now()
        time_sum, value_sum, all_up_tasks, all_hard_tasks = 0, 0, [], []
        with self.solver.use_incremental(encoding_data, self.measure) as solver:
            for report in [get_propagation(solver, backdoor) for backdoor in backdoors]:
                time, value, status, (up_tasks, hard_tasks) = report
                time_sum, value_sum = time_sum + time, value_sum + value
                all_up_tasks.extend(up_tasks), all_hard_tasks.append(hard_tasks)
            all_hard_tasks = sorted(all_hard_tasks, key=len, reverse=True)

            # todo: accumulate using executor
            [acc_hard_tasks, *all_hard_tasks] = all_hard_tasks
            for hard_tasks, count in [(ts, len(ts)) for ts in all_hard_tasks]:
                hard_tasks_count = count * len(acc_hard_tasks)
                acc_hard_tasks = [
                    concat(*parts) for parts in product(acc_hard_tasks, hard_tasks)
                    if solver.propagate(concat(*parts))[2] == Status.SOLVED
                ]
                ratio = round(len(acc_hard_tasks) / hard_tasks_count, 2)
                print(f'reduced: {hard_tasks_count} -> {len(acc_hard_tasks)} (x{ratio})')

        split_into = ceil(len(acc_hard_tasks) / self.executor.max_workers)
        for future in self.executor.submit_all(hard_worker, *(
                (self.solver, self.measure, self.instance, all_up_tasks, hard_tasks)
                for hard_tasks in slice_by(acc_hard_tasks, split_into)
        )).as_complete():
            time, value, _, _ = future.result()
            time_sum, value_sum = time_sum + time, value_sum + value

        return {
            'value': time_sum,
            'time_sum': time_sum,
            'value_sum': value_sum,
            'real_time': now() - start_stamp,
            'hard_tasks': len(acc_hard_tasks),
            'total_tasks': 2 ** len(total_var_set)
        }

    def __config__(self) -> Dict[str, Any]:
        return {}


__all__ = [
    'Combine'
]
