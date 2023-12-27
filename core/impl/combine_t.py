import os
import json

from time import time as now
from tempfile import NamedTemporaryFile
from typing import Any, List, Dict, Optional, Tuple, Iterable

from space.model import Backdoor
from ..abc import Core

from output import Logger
from executor import Executor

from lib_satprob.problem import Problem
from lib_satprob.encoding import Clauses
from lib_satprob.solver import Report, _Solver
from lib_satprob.derived import get_derived_by
from lib_satprob.variables import Assumptions, Supplements

from function.model import Estimation
from function.module.measure import Measure
from function.module.budget import TaskBudget, KeyLimit

from util.wrapppers import timed
from typings.searchable import Searchable
from util.iterable import slice_into, split_by

UnWeightTask = Tuple[int, Supplements]

#
# Formula patching logic (create, load and initialize solver)
# ==============================================================================
FORMULAS: Dict[int, Any] = {}
VERSIONS: Dict[int, Clauses] = {}


def create_patch(
        clauses: Clauses
) -> Tuple[str, int]:
    version = max(VERSIONS.keys()) \
        if len(VERSIONS) > 0 else 1
    VERSIONS[version] = clauses

    with NamedTemporaryFile(
            delete=False, mode='w+'
    ) as handle:
        json.dump(clauses, handle)
        return handle.name, version


def get_formula(
        problem: Problem,
        filename: str,
        version: int,
) -> Any:
    if version not in FORMULAS:
        print('loading...', version, filename)
        formula = problem.encoding.get_formula()
        if filename is not None and version > 0:
            with open(filename, 'r+') as handle:
                clauses = json.load(handle)
            formula.extend(clauses)

        FORMULAS[version] = formula

    return FORMULAS[version]


# def get_solver(
#         problem: Problem,
#         filename: str,
#         version: int,
# ) -> _Solver:
#     if version not in SOLVERS:
#         for solver in SOLVERS.values():
#             solver.__exit__()
#         SOLVERS.clear()
#
#         formula = get_formula(problem, filename, version)
#         solver = problem.solver.get_instance(formula)
#         SOLVERS[version] = solver.__enter__()
#
#     return SOLVERS[version]


#
# Hard task product logic (combine, worker)
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

def prod_combine(
        acc_tasks: List[Assumptions], tasks: List[Assumptions]
) -> Iterable[Supplements]:
    for assumptions in map(set, tasks):
        for acc_assumptions in acc_tasks:
            if sum([
                -literal in assumptions for
                literal in acc_assumptions
            ]) > 0: continue

            yield assumptions.union(
                set(acc_assumptions)
            ), []


def prod_worker(
        acc_tasks: List[Assumptions], tasks: List[Assumptions],
        problem: Problem, patch: str, version: int
) -> Tuple[List[Assumptions], float]:
    _stamp, prod_hard_task = now(), []
    formula = get_formula(problem, patch, version)
    with problem.solver.get_instance(formula, False) as solver:
        for acc_hard_task in prod_combine(acc_tasks, tasks):
            report = solver.propagate(acc_hard_task)
            if report.status is None or report.status:
                # cost = 0 if len(report.model) == 0 \
                #     else calc_cost(formula, report.model)
                prod_hard_task.append(acc_hard_task[0])

    return prod_hard_task, now() - _stamp


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


def hard_worker(
        task: Assumptions, limit: KeyLimit,
        problem: Problem, patch: str, version: int
) -> Tuple[Assumptions, Report]:
    formula = get_formula(problem, patch, version)
    with problem.solver.get_instance(formula) as solver:
        return task, solver.solve((task, []), limit)


class CombineT(Core):
    slug = 'core:combine_t'

    def __init__(self, logger: Logger, measure: Measure, problem: Problem,
                 executor: Executor, budget: TaskBudget,
                 random_seed: Optional[int] = None):
        self.budget = budget
        self.measure = measure
        self.executor = executor
        super().__init__(logger, problem, random_seed)

        self.clauses = []
        self.stats_sum = {
            'prod_time': 0.,
            'grow_time': 0.
        }
        self.best_model = (None, [])

    def sifting(
            self, tasks: List[Assumptions], patch: str, version: int
    ) -> List[Assumptions]:
        hard_tasks, limit = [], self.measure.get_limit(self.budget)
        future_all, count = self.executor.submit_all(hard_worker, *(
            (task, limit, self.problem, patch, version) for task in tasks
        )), len(tasks)
        print('weight penalty:', f'{len(tasks)} -> {len(future_all)}')

        while len(future_all) > 0:
            for future in future_all.as_complete(count=1):
                task, report = future.result()
                for key, value in report.stats.items():
                    self.stats_sum[key] = \
                        self.stats_sum.get(key, 0.) + value

                if report.status is None: hard_tasks.append(task)
                if report.cost and report.cost < self.best_model[0]:
                    bsu = f'{self.best_model[0]} -> {report.cost}'
                    self.best_model = (report.cost, report.model)
                    print('best solution upd:', bsu, f'{report.cost}')

                hrd, left = len(hard_tasks), len(future_all)
                print(f'{hrd}/{hrd + left}/{count}: {report}')

        return hard_tasks

    def _preprocess(self, *backdoors: Backdoor) -> List[List[Assumptions]]:
        current_var_set, all_hard_tasks = set(), []
        all_assumptions, all_constraints = set(), set()

        def var_distance(_searchable: Searchable) -> int:
            return sum([
                0 if var.name in current_var_set else
                1 for var in _searchable.variables()
            ])

        results = [future.result() for future in self.executor.submit_all(
            prep_worker, *((self.problem, bd) for bd in backdoors)
        ).as_complete()]
        one_hard, results = split_by(results, lambda r: len(r[2]) == 1)
        processed = sorted(results, key=lambda r: len(r[2]))

        def add_supplements(_supplements: Supplements):
            _assumptions, _constraints = _supplements
            all_assumptions.update(set(_assumptions))
            for _clause in map(tuple, _constraints):
                all_constraints.add(_clause)
            for _var in map(abs, _assumptions):
                current_var_set.add(_var)

        for searchable, _, hard_tasks in one_hard:
            add_supplements(hard_tasks[0])

        for future in self.executor.submit_all(timed(get_derived_by), *(
                (easy_tasks,) for _, easy_tasks, _ in processed
        )).as_complete():
            supplements, _time = future.result()
            self.stats_sum['grow_time'] += _time
            add_supplements(supplements)

        print(all_assumptions)

        for searchable, _, hard_tasks in processed:
            fil_hard_tasks = []
            for hard_task in hard_tasks:
                fil_hard_task = []
                for literal in hard_task[0]:
                    if -literal in all_assumptions:
                        break
                    if literal not in all_assumptions:
                        fil_hard_task.append(literal)
                else:
                    print(hard_task[0], '->', fil_hard_task)
                    fil_hard_tasks.append((fil_hard_task, []))

            print(searchable, len(hard_tasks), '->', len(fil_hard_tasks))

            if var_distance(searchable) > 1:
                all_hard_tasks.append(fil_hard_tasks)
                for var in searchable.variables():
                    current_var_set.add(var.name)

        # if len(all_assumptions) > 0:
        #     assumptions = list(all_assumptions)
        #     # all_hard_tasks.insert(0, [(assumptions, [])])

        # if len(all_constraints) > 0:
        #     constraints = map(list, all_constraints)

        constraints = map(list, all_constraints)
        self.clauses = list(constraints) + [
            [lit] for lit in all_assumptions
        ]

        return [
            [task[0] for task in tasks]
            for tasks in all_hard_tasks
        ]

    def launch(self, *backdoors: Backdoor) -> Estimation:
        start_stamp, files = now(), []
        # self.best_model = (sum(formula.wght), [])
        try:
            all_hard_tasks = self._preprocess(*backdoors)
            [acc_hard_tasks, *all_hard_tasks] = all_hard_tasks

            if len(self.clauses) > 0:
                patch_file, version = create_patch(self.clauses)
            else:
                patch_file, version = None, 0

            plot_data = [(
                len(set(map(abs, acc_hard_tasks[0]))),
                len(acc_hard_tasks), len(acc_hard_tasks)
            )]

            for i, hard_tasks in enumerate(all_hard_tasks):
                next_acc_hard_tasks = []
                prod_size = len(acc_hard_tasks) * len(hard_tasks)
                # print(acc_hard_tasks, 'x', hard_tasks)

                for future in self.executor.submit_all(prod_worker, *((
                        acc_part_hard_tasks, hard_tasks,
                        self.problem, patch_file, version
                ) for acc_part_hard_tasks in slice_into(
                    acc_hard_tasks, self.executor.max_workers
                ))).as_complete():
                    prod_tasks, prod_time = future.result()
                    self.stats_sum['prod_time'] += prod_time
                    next_acc_hard_tasks.extend(prod_tasks)

                var_set = sorted(set(map(abs, next_acc_hard_tasks[0])))
                print(f'var set ({len(var_set)}):', ' '.join(map(str, var_set)))
                print('stats:', self.stats_sum)
                print(f'time ({self.executor.max_workers})',
                      now() - start_stamp)

                print(
                    f'reduced: {prod_size} -> {len(next_acc_hard_tasks)}',
                    f'({round(len(next_acc_hard_tasks) / prod_size, 2)})',
                )
                acc_hard_tasks = self.sifting(
                    next_acc_hard_tasks, patch_file, version
                )

                plot_data.append((
                    len(var_set), len(next_acc_hard_tasks), len(acc_hard_tasks)
                ))

                print(
                    f'sifted: {len(next_acc_hard_tasks)} -> {len(acc_hard_tasks)}',
                    f'({round(len(acc_hard_tasks) / len(next_acc_hard_tasks), 2)})'
                )
                if len(acc_hard_tasks) == 0:
                    print(f'total bds: {i + 1}')
                    print('total stats:', self.stats_sum)
                    print(f'total time ({self.executor.max_workers})',
                          now() - start_stamp)
                    print(f'total var set ({len(var_set)}):',
                          ' '.join(map(str, var_set)))
                    break

            print(self.stats_sum)
            print(self.best_model)
            print('parallel time:', now() - start_stamp)
            print('sequential time:', self.stats_sum['grow_time'] +
                  self.stats_sum['time'] + self.stats_sum['prod_time'])

            print('plot data')
            print(json.dumps(plot_data))

            return self.stats_sum
        finally:
            [os.remove(file) for file in files]

    def __config__(self) -> Dict[str, Any]:
        return {}


__all__ = [
    'CombineT'
]
