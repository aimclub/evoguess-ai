from math import ceil
from time import time as now
from itertools import product
from typing import Any, List, Dict, Optional, Tuple

from output import Logger
from executor import Executor

from ..abc import Core

from lib_satprob.solver import Report
from lib_satprob.problem import Problem
from lib_satprob.variables import Supplements, combine

from typings.searchable import Searchable
from utility.iterable import concat, slice_by, slice_into


def prep_worker(problem: Problem, searchable: Searchable) -> List[Supplements]:
    clauses = problem.encoding.get_formula(copy=False)
    with problem.solver.get_instance(clauses) as solver:
        hard_filter = lambda st: st is None or st
        return [sups for sups in searchable.enumerate()
                if hard_filter(solver.propagate(sups).status)]


def prod_worker(
        problem: Problem, acc_tasks: List[Supplements], tasks: List[Supplements]
) -> Tuple[List[Supplements], float]:
    _stamp, formula = now(), problem.encoding.get_formula(copy=False)
    w_acc_hard_task, prod = [], product(acc_tasks, tasks)

    with problem.solver.get_instance(formula) as solver:
        for acc_hard_task in [combine(*prs) for prs in prod]:
            report = solver.propagate(acc_hard_task)
            if report.status is None or report.status:
                w_acc_hard_task.append(acc_hard_task)

    return w_acc_hard_task, now() - _stamp


def hard_worker(problem: Problem, hard_tasks: List[Supplements]) -> Report:
    hard_status, hard_model, hard_cost = False, None, None
    stats_sum, formula = {}, problem.encoding.get_formula()
    with problem.solver.get_instance(formula) as incremental:
        for i, supplements in enumerate(hard_tasks):
            status, stats, model, cost = incremental.solve(
                supplements, extract_model=False
            )
            for key, value in stats.items():
                stats_sum[key] = stats_sum.get(key, 0.) + value

            if status:
                hard_cost = cost
                hard_model = model
                hard_status = True

    return Report(hard_status, stats_sum, hard_model, hard_cost)


class Combine(Core):
    slug = 'core:combine'

    def __init__(self, logger: Logger, problem: Problem,
                 executor: Executor, random_seed: Optional[int] = None):
        self.executor = executor
        super().__init__(logger, problem, random_seed)

        self.stats_sum = {}

    def launch(self, *searchables: Searchable) -> Report:
        total_var_set, start_stamp = set(concat(*searchables)), now()
        results = [future.result() for future in self.executor.submit_all(
            prep_worker, *((self.problem, sch) for sch in searchables)
        ).as_complete()]

        all_hard_tasks = sorted(results, key=len)
        [acc_hard_tasks, *all_hard_tasks] = all_hard_tasks

        for i, hard_tasks in enumerate(all_hard_tasks):
            next_acc_hard_tasks = []
            prod_size = len(acc_hard_tasks) * len(hard_tasks)
            for future in self.executor.submit_all(prod_worker, *((
                    self.problem, acc_part_hard_tasks, hard_tasks
            ) for acc_part_hard_tasks in slice_into(
                acc_hard_tasks, self.executor.max_workers
            ))).as_complete():
                prod_tasks, prod_time = future.result()
                # self.stats_sum['prod_time'] += prod_time
                next_acc_hard_tasks.extend(prod_tasks)

            acc_hard_tasks = next_acc_hard_tasks
            ratio = round(len(acc_hard_tasks) / prod_size, 2)
            print(f'reduced: {prod_size} -> {len(acc_hard_tasks)} (x{ratio})')

        hard_status, hard_model, hard_cost = False, None, None
        split_into = ceil(len(acc_hard_tasks) / self.executor.max_workers)
        for future in self.executor.submit_all(hard_worker, *(
                (self.problem, hard_tasks) for hard_tasks
                in slice_by(acc_hard_tasks, split_into)
        )).as_complete():
            status, stats, model, cost = future.result()
            for key, value in stats.items():
                self.stats_sum[key] = \
                    self.stats_sum.get(key, 0.) + value

            if status:
                hard_cost = cost
                hard_model = model
                hard_status = True

        self.stats_sum['count'] = len(acc_hard_tasks)
        self.stats_sum['real_time'] = now() - start_stamp
        return Report(hard_status, self.stats_sum, hard_model, hard_cost)

    def __config__(self) -> Dict[str, Any]:
        return {}


__all__ = [
    'Combine'
]
