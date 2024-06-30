import os
from concurrent.futures import ProcessPoolExecutor

from math import ceil
from typing import Any, List, \
    Dict, Optional, Tuple, Iterable

from ..abc import Core
from output import Logger
from space.model import Backdoor

from lib_satprob.solver import Report
from lib_satprob.problem import Problem
from lib_satprob.encoding.patch import SatPatch
from lib_satprob.variables import Assumptions, Supplements

from function.module.measure import Measure
from function.module.budget import TaskBudget, KeyLimit, UNLIMITED

from utility.polyfill import tqdm
from utility.wrappers import timed, untime
from utility.iterable import slice_into, split_by
from utility.format import printc, passed, time_ms

from rho_tool import rho_fn_ext
from rho_tool.rho_order import rho_preprocess
from rho_tool.rho_pool import init_process_pool, get_process_state

UnWeightTask = Tuple[int, Supplements]


#
# Utility (chunked mapper)
# ==============================================================================
def chunked_map(executor, fn, *iterables):
    chunk_size = ceil(len(iterables) / executor._max_workers)
    return executor.map(fn, iterables, chunksize=chunk_size)


#
#
# ==============================================================================
# def _print(*args):
#     s = ' '.join(map(str, args))
#     print(s)
#     with open('w_log.txt', 'a+') as hndl:
#         hndl.write(f'{s}\n')


#
# ==============================================================================
# def is_unsat(clause: List[int], value_map: Dict[int, int]) -> bool:
#     size = len(clause)
#     for literal in clause:
#         value = value_map.get(abs(literal))
#         if literal == value:
#             return False
#         if value is not None:
#             size -= 1
#     return True if size == 0 else None


# def calc_cost(formula, literals: Assumptions) -> int:
#     value_map = {abs(lit): lit for lit in literals}
#     return sum([
#         weight if is_unsat(clause, value_map) else 0 for
#         weight, clause in zip(formula.wght, formula.soft)
#     ])

#
# Product task logic (combine, worker)
# ==============================================================================
def prod_combine(
        acc_tasks: List[Supplements],
        tasks: List[Supplements]
) -> Iterable[Supplements]:
    a_list = [set(t[0]) for t in tasks]
    for assumptions in a_list:
        for acc_assumptions in acc_tasks:
            if sum([
                -literal in assumptions for
                literal in acc_assumptions[0]
            ]) > 0: continue

            yield assumptions.union(
                set(acc_assumptions[0])
            ), []


def prod_fn(
        patch: SatPatch,
        tasks: List[Supplements],
        acc_tasks: List[Supplements]
) -> List[Supplements]:
    get_process_state().apply_patch(patch)
    sub_solver = get_process_state().sub_solver
    # cost = 0 if len(report.model) == 0 \
    #     else calc_cost(formula, report.model)
    return [
        task for task in prod_combine(acc_tasks, tasks)
        if sub_solver.propagate(task).status is not False
    ]


#
# ==============================================================================
def prep_worker(
        problem: Problem, backdoor: Backdoor
) -> Tuple[Backdoor, List[Supplements], List[Supplements]]:
    formula = problem.encoding.get_formula(copy=False)
    with problem.solver.get_instance(formula) as solver:
        easy, hard = split_by(
            backdoor.enumerate(), lambda sups:
            solver.propagate(sups).status is False
        )
        return backdoor, easy, hard


def hard_worker_inc(
        patch: SatPatch,
        task: Supplements,
        limit: KeyLimit
) -> Tuple[Supplements, Report]:
    get_process_state().apply_patch(patch)
    solver = get_process_state().solver

    return task, solver.solve(task, limit)


def hard_worker(
        patch: SatPatch,
        task: Supplements,
        limit: KeyLimit,
) -> Tuple[Supplements, Report]:
    problem = get_process_state().problem
    formula = problem.encoding.get_formula(patch=patch)
    with problem.solver.get_instance(formula) as solver:
        return task, solver.solve(task, limit)


class CombineT(Core):
    slug = 'core:combine_t'

    def __init__(self, logger: Logger, problem: Problem, measure: Measure,
                 budget: TaskBudget, random_seed: Optional[int] = None,
                 max_workers: Optional[int] = None):
        self.budget, self.measure = budget, measure
        super().__init__(logger, problem, random_seed)

        self.clauses = []
        self.stats_sum = {
            'prod_time': 0.,
            'grow_time': 0.
        }
        self.solutions = []
        self.best_model = (None, [])
        self.max_workers = max_workers

    def sifting(
            self, patch: SatPatch,
            tasks: List[Assumptions],
            executor: ProcessPoolExecutor,
            is_last_iter: bool = False
    ) -> List[Supplements]:
        hard_tasks, tqdm_kwargs, limit = [], {
            'desc': 'Sifting', 'postfix': '0 hard',
            'total': len(tasks), 'unit': 'task',
        }, self.measure.get_limit(self.budget)

        with tqdm(**tqdm_kwargs) as progress:
            limit = UNLIMITED if is_last_iter else limit
            for task, report in executor.map(hard_worker, *zip(*(
                    (patch, task, limit) for task in tasks
            ))):
                for key, value in report.stats.items():
                    self.stats_sum[key] = \
                        self.stats_sum.get(key, 0.) + value

                progress.update()
                if report.status is None:
                    hard_tasks.append(task)
                    progress.set_postfix_str(
                        f'{len(hard_tasks)} hard'
                    )
                if report.status is True:
                    self.logger.write(report, passed())

        return hard_tasks

    def process(self, patch: SatPatch, hard_order: List[Supplements],
                executor: ProcessPoolExecutor) -> Report:
        workers = self.max_workers or executor._max_workers

        if len(hard_order) == 0:
            formula = self.problem.encoding.get_formula(patch=patch)
            solver = self.problem.solver.get_instance(formula)
            return solver.solve(([], []))

        [acc_hard_tasks, *hard_order] = hard_order
        var_set = set(map(abs, acc_hard_tasks[0][0]))
        for i, hard_tasks in enumerate(hard_order):
            next_acc_hard_tasks, prod_real_size = \
                [], len(acc_hard_tasks) * len(hard_tasks)

            is_last_iter = (i + 1 == len(hard_order))
            var_set.update(set(map(abs, hard_tasks[0][0])))
            printc(f'Used {i + 2} backdoors ({len(var_set)} vars)')
            for result in executor.map(timed(prod_fn), *zip(*(
                    (patch, hard_tasks, sliced) for sliced
                    in slice_into(acc_hard_tasks, workers)
            ))):
                prod_tasks, prod_time = result
                self.stats_sum['prod_time'] += prod_time
                next_acc_hard_tasks.extend(prod_tasks)

            if is_last_iter: printc(
                f'Disable solver budget (last backdoor)'
            )
            acc_hard_tasks = self.sifting(
                patch, next_acc_hard_tasks,
                executor, is_last_iter
            )

            if len(acc_hard_tasks) == 0:
                status = len(self.solutions) > 0
                model = self.solutions if status else None
                return Report(status, self.stats_sum, model)

        if len(acc_hard_tasks) > 0:
            self.sifting(patch, acc_hard_tasks, executor, True)
            status = len(self.solutions) > 0
            model = self.solutions if status else None
            return Report(status, self.stats_sum, model)

    def launch(self, *backdoors: Backdoor) -> Report:
        workers = self.max_workers or os.cpu_count()
        executor = init_process_pool(self.problem, workers)
        rho_args = (executor, timed(rho_fn_ext), *backdoors)
        points, rho_fn_time = untime(chunked_map(*rho_args))
        patch, hard_order = rho_preprocess(set(), points, executor)

        pre_stamp, derive_time = time_ms(), passed()
        self.logger.meta(self.problem, *points)

        try:
            return self.process(
                patch,
                hard_order,
                executor
            )
        finally:
            del patch

    def __config__(self) -> Dict[str, Any]:
        return {}


__all__ = [
    'CombineT'
]
