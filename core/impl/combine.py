from math import ceil
from time import time as now
from typing import Any, List, Dict, Optional
from itertools import chain, product

from output import Logger
from executor import Executor

from ..abc import Core

from function.module.measure import Measure
from function.model import Status, Estimation

from pysatmc.problem import Problem
from pysatmc.variables import Assumptions
from pysatmc.solver import Solver, _Solver, Report

from typings.searchable import Searchable
from util.iterable import concat, slice_by


def get_propagation(solver: _Solver, searchable: Searchable) -> Report:
    time_sum, value_sum, up_tasks, hard_tasks = 0, 0, [], []
    for supplements in searchable.enumerate():
        status, stats, _ = solver.propagate(supplements)
        (up_tasks if status else hard_tasks).append(supplements)
        time_sum, value_sum = time_sum + time, value_sum + value

    status = len(hard_tasks) == 0
    return Report(status, stats, (up_tasks, hard_tasks))


def hard_worker(solver: Solver, problem: Problem, up_tasks: List[Assumptions],
                hard_tasks: List[Assumptions]) -> Report:
    time_sum, value_sum, formula = 0, 0, problem.encoding.get_formula()
    with solver.get_instance(formula) as incremental:
        for up_task_assumptions in chain(up_tasks, hard_tasks):
            time, value, _, _ = incremental.solve(
                (up_task_assumptions, []), extract_model=False
            )
            time_sum, value_sum = time_sum + time, value_sum + value

    return Report(time_sum, value_sum, Status.RESOLVED, None)


class Combine(Core):
    slug = 'core:combine'

    def __init__(self, logger: Logger, measure: Measure, problem: Problem,
                 executor: Executor, random_seed: Optional[int] = None):
        self.measure = measure
        self.executor = executor
        super().__init__(logger, problem, random_seed)

    def launch(self, *searchables: Searchable) -> Estimation:
        formula = self.problem.encoding.get_formula()
        total_var_set, start_stamp = set(concat(*searchables)), now()
        time_sum, value_sum, all_up_tasks, all_hard_tasks = 0, 0, [], []
        with self.problem.solver.get_instance(formula) as solver:
            for searchable in searchables:
                report = get_propagation(solver, searchable)
                time, value, status, (up_tasks, hard_tasks) = report
                time_sum, value_sum = time_sum + time, value_sum + value
                all_up_tasks.extend(up_tasks), all_hard_tasks.append(hard_tasks)
            all_hard_tasks = sorted(all_hard_tasks, key=len, reverse=True)

            # todo: accumulate using executor
            [acc_hard_tasks, *all_hard_tasks] = all_hard_tasks
            for hard_tasks, count in [(ts, len(ts)) for ts in all_hard_tasks]:
                hard_tasks_count = count * len(acc_hard_tasks)
                acc_hard_tasks = [
                    concat(*parts) for parts in
                    product(acc_hard_tasks, hard_tasks)
                    if solver.propagate((concat(*parts), [])).status
                ]
                ratio = round(len(acc_hard_tasks) / hard_tasks_count, 2)
                print(
                    f'reduced: {hard_tasks_count} -> {len(acc_hard_tasks)} (x{ratio})')

        split_into = ceil(len(acc_hard_tasks) / self.executor.max_workers)
        for future in self.executor.submit_all(hard_worker, *(
                (self.solver, self.problem, all_up_tasks, hard_tasks)
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
