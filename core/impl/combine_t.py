import json
from time import time as now
from typing import Any, List, Dict, Optional, Tuple
from itertools import product

from output import Logger
from executor import Executor

from ..abc import Core

from function.model import Estimation
from function.module.budget import TaskBudget, KeyLimit
from function.module.measure import Measure

from pysatmc.solver import Report
from pysatmc.problem import Problem
from pysatmc.variables import Assumptions, Supplements

from typings.searchable import Searchable
from util.iterable import concat, slice_by

IndexTask = Tuple[int, Supplements]

TaskSlice = Tuple[List[Supplements], List[Supplements]]
IndexTaskSlice = Tuple[List[IndexTask], List[IndexTask]]


def propagate(problem: Problem, searchable: Searchable) -> TaskSlice:
    up_tasks, no_up_tasks = [], []
    formula = problem.encoding.get_formula(copy=False)
    with problem.solver.get_instance(formula.hard) as solver:
        for supplements in searchable.enumerate():
            status, _, _ = solver.propagate(supplements)
            if status is None or status:
                no_up_tasks.append(supplements)
            else:
                up_tasks.append(supplements)

    return up_tasks, no_up_tasks


def limit_worker(problem: Problem, index_task: Tuple[int, Supplements],
                 limit: KeyLimit) -> Tuple[Tuple[int, Supplements], Report]:
    formula = problem.encoding.get_formula(copy=False)
    with problem.solver.get_instance(formula) as solver:
        return index_task, solver.solve(index_task[1], limit)


def hard_worker(problem: Problem, hard_task: Assumptions) -> Report:
    formula = problem.encoding.get_formula(copy=False)
    return problem.solver.solve(formula, (hard_task, []))


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
        time_sum, value_sum, all_hard_dict = 0, 0, {}
        total_var_set, start_stamp = set(concat(*searchables)), now()

        all_no_up_tasks = []
        with self.logger:
            for index, searchable in enumerate(searchables):
                _, no_up_tasks = propagate(self.problem, searchable)
                all_no_up_tasks.extend(
                    (index, no_up_task) for
                    no_up_task in no_up_tasks
                )
                all_hard_dict[index] = []
                print(searchable, len(no_up_tasks))

            stats_sum, limit = {}, self.measure.get_limit(self.budget)
            future_all, i = self.executor.submit_all(limit_worker, *(
                (self.problem, task, limit) for task in all_no_up_tasks
            )), 0
            while len(future_all) > 0:
                for future in future_all.as_complete(timeout=5):
                    (index, supplements), report = future.result()
                    tv = self.measure.check_and_get(report, self.budget)
                    time_sum, value_sum = time_sum + tv[0], value_sum + tv[1]

                    i, (status, _, model) = i + 1, report
                    if status is None: all_hard_dict[index].append(supplements)
                    _model = len(model) if status else ''
                    print(f'{i}/{len(all_no_up_tasks)}: {status}', end='')
                    print(', time:', time_sum, 'value:', value_sum)

            all_hard_tasks = []
            for index, hard_tasks in all_hard_dict.items():
                print(f'{index}({len(hard_tasks)}): {hard_tasks}')
                all_hard_tasks.append([a for a, c in hard_tasks])

            print('time:', time_sum, 'value:', value_sum)
            formula = self.problem.encoding.get_formula()
            all_hard_tasks = sorted(all_hard_tasks, key=len, reverse=True)
            with self.problem.solver.get_instance(formula.hard) as solver:
                [acc_hard_tasks, *all_hard_tasks] = all_hard_tasks
                for hard_tasks in all_hard_tasks:
                    acc_hard_tasks = [
                        concat(*parts) for parts in
                        product(acc_hard_tasks, hard_tasks)
                    ]

                    no_up_acc_hard_task = []
                    for acc_hard_task in acc_hard_tasks:
                        status, _, _ = solver.propagate((acc_hard_task, []))
                        if status is None or status:
                            no_up_acc_hard_task.append(acc_hard_task)

                    ratio = round(
                        len(no_up_acc_hard_task) / len(acc_hard_tasks), 2)
                    suf_str = f'{len(no_up_acc_hard_task)} (x{ratio})'
                    print(f'reduced: {len(acc_hard_tasks)} -> {suf_str}')
                    acc_hard_tasks = no_up_acc_hard_task

            filename = 'hard_tasks_prod.jsonl'
            if self.logger._session is not None:
                filepath = self.logger._session.to_file(filename)
                with open(filepath, 'a+') as handle:
                    for hard_task in acc_hard_tasks:
                        string = json.dumps({
                            "assumptions": hard_task
                        })
                        handle.write(f'{string}\n')

            future_all, i = self.executor.submit_all(hard_worker, *(
                (self.problem, hard_task) for hard_task in acc_hard_tasks
            )), 0
            while len(future_all) > 0:
                for future in future_all.as_complete(count=1):
                    report = future.result()
                    i, (status, _, model) = i + 1, report
                    print(f'{i}/{len(acc_hard_tasks)}: {report}')
                    tv = self.measure.check_and_get(report, self.budget)
                    time_sum, value_sum = time_sum + tv[0], value_sum + tv[1]

            result = {
                'value': time_sum,
                'time_sum': time_sum,
                'value_sum': value_sum,
                'real_time': now() - start_stamp,
                'hard_tasks': len(acc_hard_tasks),
                'total_tasks': 2 ** len(total_var_set)
            }
            self.logger._format(result, filename='result.jsonl')
            return result

    def __config__(self) -> Dict[str, Any]:
        return {}


__all__ = [
    'CombineT'
]
