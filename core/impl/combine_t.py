from math import ceil
from time import time as now
from typing import Any, List, Dict, Optional
from itertools import product

from output import Logger
from executor import Executor

from ..abc import Core

from function.model import Estimation
from function.module.budget import TaskBudget
from function.module.measure import Measure

from pysatmc.solver import Report
from pysatmc.problem import Problem
from pysatmc.variables import Assumptions

from typings.searchable import Searchable
from util.iterable import concat, slice_by


def hard_worker(problem: Problem, hard_tasks: List[Assumptions]) -> Report:
    stats_sum, formula = {}, problem.encoding.get_formula()
    with problem.solver.get_instance(formula) as solver:
        for assumptions in hard_tasks:
            _, stats, _ = solver.solve((assumptions, []))
            for key in set(stats_sum.keys()).union(stats.keys()):
                stats_sum[key] = stats_sum.get(key, 0) + stats.get(key, 0)

    return Report(True, stats_sum, None)


class CombineT(Core):
    slug = 'core:combine'

    def __init__(self, logger: Logger, measure: Measure, problem: Problem,
                 executor: Executor, budget: TaskBudget,
                 random_seed: Optional[int] = None):
        self.budget = budget
        self.measure = measure
        self.executor = executor
        super().__init__(logger, problem, random_seed)

    def launch(self, *searchables: Searchable) -> Estimation:
        formula = self.problem.encoding.get_formula()
        time_sum, value_sum, all_hard_tasks = 0, 0, []
        total_var_set, start_stamp = set(concat(*searchables)), now()
        with self.problem.solver.get_instance(formula) as solver:
            limit = self.measure.get_limit(self.budget)
            for searchable in searchables:
                index, count, hard_tasks = 0, 0, []
                for supplements in searchable.enumerate():
                    report = solver.solve(supplements, limit)
                    tv = self.measure.check_and_get(report, self.budget)
                    time_sum, value_sum = time_sum + tv[0], value_sum + tv[1]
                    if report.status is None:
                        assumptions, _ = supplements
                        hard_tasks.append(assumptions)

                    index += 1
                    count += (1 if report.model else 0)
                    print(f'{count}/{index}', report)

                print(searchable, 'hard:', len(hard_tasks))
                all_hard_tasks.append(hard_tasks)

            all_hard_tasks = sorted(all_hard_tasks, key=len, reverse=True)

            [acc_hard_tasks, *all_hard_tasks] = all_hard_tasks
            for hard_tasks, count in [(ts, len(ts)) for ts in all_hard_tasks]:
                ht_count = count * len(acc_hard_tasks)
                acc_hard_tasks = [
                    concat(*parts) for parts in
                    product(acc_hard_tasks, hard_tasks)
                    if solver.propagate((concat(*parts), [])).status
                ]
                ratio = round(len(acc_hard_tasks) / ht_count, 2)
                print(
                    f'reduced: {ht_count} -> {len(acc_hard_tasks)} (x{ratio})')

        split_into = ceil(len(acc_hard_tasks) / self.executor.max_workers)
        for future in self.executor.submit_all(hard_worker, *(
                (self.problem, hard_tasks) for hard_tasks
                in slice_by(acc_hard_tasks, split_into)
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
    'CombineT'
]
