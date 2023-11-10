import os
import json

from time import time as now
from itertools import product
from tempfile import NamedTemporaryFile as NTFile
from typing import Any, List, Dict, Optional, Tuple

from output import Logger
from executor import Executor
from pysatmc.encoding import WCNF

from ..abc import Core

from pysatmc.solver import Report
from pysatmc.problem import Problem
from pysatmc.variables import Assumptions, Supplements, combine

from function.model import Estimation
from function.module.measure import Measure
from function.module.budget import TaskBudget, KeyLimit

from typings.searchable import Searchable
from util.iterable import slice_into, split_by

UnWeightTask = Tuple[int, Supplements]


#
#
#
def bool2sign(b):
    return -1 if b else 1


def signed(x, s):
    return bool2sign(s) * x


def minimize_dnf(dnf):
    from pyeda.inter import espresso_exprs

    min_dnf = espresso_exprs(dnf)
    return min_dnf


def cnf_to_clauses(cnf):
    assert cnf.is_cnf()

    litmap, nvars, clauses = cnf.encode_cnf()
    result = []
    for clause in clauses:
        c = []
        for lit in clause:
            v = litmap[abs(lit)].indices[0]  # 1-based variable index
            s = lit < 0  # sign
            c.append(signed(v, s))
        c.sort(key=lambda x: abs(x))
        result.append(c)

    clauses = result
    clauses.sort(key=lambda x: (len(x), tuple(map(abs, x))))
    return clauses


def cubes_to_dnf(cubes):
    from pyeda.inter import exprvar, And, Or

    var_map = dict()
    cubes_expr = []

    for cube in cubes:
        lits_expr = []
        for lit in cube:
            var = abs(lit)
            if var not in var_map:
                var_map[var] = exprvar("x", var)
            if lit < 0:
                lits_expr.append(~var_map[var])
            else:
                lits_expr.append(var_map[var])
        cubes_expr.append(And(*lits_expr))

    dnf = Or(*cubes_expr)
    assert dnf.is_dnf()
    return dnf


def backdoor_to_clauses_via_easy(easy):
    # Note: here, 'dnf' represents the negation of characteristic function,
    #       because we use "easy" tasks here.
    dnf = cubes_to_dnf(easy)
    (min_dnf,) = minimize_dnf(dnf)
    min_cnf = (~min_dnf).to_cnf()  # here, we negate the function back
    clauses = cnf_to_clauses(min_cnf)
    return clauses


def grow_worker(easy_tasks: List[Supplements]) -> Tuple[Supplements, float]:
    _stamp, easy_cubes = now(), [sups[0] for sups in easy_tasks]
    clauses = backdoor_to_clauses_via_easy(easy_cubes)
    constr, one_lit = split_by(clauses, lambda x: len(x) > 1)
    return ([clause[0] for clause in one_lit], constr), now() - _stamp


#
#
#


def is_sat(clause: List[int], solution: List[int]) -> bool:
    for literal in clause:
        if literal in solution:
            return True
    return False


def is_unsat(clause: List[int], value_map: Dict[int, int]) -> bool:
    size = len(clause)
    for literal in clause:
        value = value_map.get(abs(literal))
        if literal == value:
            return False
        if value is not None:
            size -= 1
    return True if size == 0 else None


def calc_count(formula, solution: Assumptions) -> int:
    return sum([
        is_sat(clause, solution) for clause in formula.soft
    ])


def calc_weight(formula, solution: Assumptions) -> int:
    return sum([
        weight if is_sat(clause, solution) else 0 for
        weight, clause in zip(formula.wght, formula.soft)
    ])


def calc_unweight(formula, literals: Assumptions) -> int:
    value_map = {abs(lit): lit for lit in literals}
    return sum([
        weight if is_unsat(clause, value_map) else 0 for
        weight, clause in zip(formula.wght, formula.soft)
    ])


def prep_worker(
        problem: Problem, searchable: Searchable
) -> Tuple[Searchable, List[Supplements], List[Supplements]]:
    clauses = problem.encoding.get_formula(copy=False).hard
    with problem.solver.get_instance(clauses) as solver:
        easy, hard = split_by(
            searchable.enumerate(), lambda sups:
            solver.propagate(sups).status is False
        )
        return searchable, easy, hard


def prod_worker(
        problem: Problem, acc_tasks: List[UnWeightTask],
        tasks: List[UnWeightTask],
) -> Tuple[List[UnWeightTask], float]:
    tasks, acc_tasks = [t[1] for t in tasks], [t[1] for t in acc_tasks]
    _stamp, formula = now(), problem.encoding.get_formula(copy=False)
    w_acc_hard_task, prod = [], product(acc_tasks, tasks)

    with problem.solver.get_instance(formula.hard) as solver:
        for acc_hard_task in [combine(*prs) for prs in prod]:
            report = solver.propagate(acc_hard_task)
            if report.status is None or report.status:
                unweight = 0 if len(report.model) == 0 \
                    else calc_unweight(formula, report.model)
                w_acc_hard_task.append((unweight, acc_hard_task))

    return w_acc_hard_task, now() - _stamp


def limit_worker(
        problem: Problem, task: UnWeightTask, limit: KeyLimit
) -> Tuple[UnWeightTask, Report]:
    formula = problem.encoding.get_formula(copy=False)
    with problem.solver.get_instance(formula) as solver:
        status, stats, _, _ = solver.solve(task[1], limit, extract_model=False)
        # if status: weight = None
        return task, Report(status, stats, None, None)


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

        self.clauses = []
        self.stats_sum = {}
        self.max_weight = None
        self.best_model = (0, [])

    def sifting(self, tasks: List[UnWeightTask]) -> List[UnWeightTask]:
        hard_tasks, limit = [], self.measure.get_limit(self.budget)
        future_all, count = self.executor.submit_all(limit_worker, *(
            (self.problem, task, limit) for task in tasks if
            self.best_model[0] + task[0] < self.max_weight
        )), len(tasks)
        print('weight penalty:', f'{len(tasks)} -> {len(future_all)}')

        while len(future_all) > 0:
            for future in future_all.as_complete(count=1):
                task, report = future.result()
                for key, value in report.stats.items():
                    self.stats_sum[key] = \
                        self.stats_sum.get(key, 0.) + value

                if report.status is None: hard_tasks.append(task)
                if report.weight and report.weight > self.best_model[0]:
                    ltm = f'{self.max_weight - report.weight}'
                    bsu = f'{self.best_model[0]} -> {report.weight}'
                    self.best_model = (report.weight, report.model)
                    ratio = round(report.weight / self.max_weight, 4)
                    print('best solution upd:', bsu, f'({ratio}) -{ltm}')

                hrd, left = len(hard_tasks), len(future_all)
                print(f'{hrd}/{hrd + left}/{count}: {report}')

        return hard_tasks

    def _preprocess(self, *searchables: Searchable) -> List[List[UnWeightTask]]:
        current_var_set, all_hard_tasks = set(), []
        all_assumptions, all_constraints = set(), set()

        def var_distance(_searchable: Searchable) -> int:
            return sum([
                0 if var.name in current_var_set else
                1 for var in _searchable.variables()
            ])

        results = [future.result() for future in self.executor.submit_all(
            prep_worker, *((self.problem, sch) for sch in searchables)
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

        for future in self.executor.submit_all(grow_worker, *(
                (easy_tasks,) for _, easy_tasks, _ in processed
        )).as_complete():
            supplements, grow_time = future.result()
            self.stats_sum['grow_time'] += grow_time
            add_supplements(supplements)

        for searchable, _, hard_tasks in processed:
            if var_distance(searchable) > 1:
                all_hard_tasks.append(hard_tasks)
                for var in searchable.variables():
                    current_var_set.add(var.name)

        if len(all_assumptions) > 0:
            assumptions = list(all_assumptions)
            all_hard_tasks.insert(0, [(assumptions, [])])

        if len(all_constraints) > 0:
            constraints = map(list, all_constraints)
            self.clauses = list(constraints)

        return [
            [(0, task) for task in tasks]
            for tasks in all_hard_tasks
        ]

    def launch(self, *searchables: Searchable) -> Estimation:
        formula, files = self.problem.encoding.get_formula(), []
        self.max_weight, start_stamp = sum(formula.wght), now()
        self.stats_sum['prod_time'] = 0
        self.stats_sum['grow_time'] = 0

        with self.logger:
            all_hard_tasks = self._preprocess(*searchables)
            [acc_hard_tasks, *all_hard_tasks] = all_hard_tasks

            with NTFile(delete=False) as wcnf_file:
                formula.extend(self.clauses)
                formula.to_file(wcnf_file.name)
                files.append(wcnf_file.name)
                self.problem.encoding = WCNF(
                    from_file=wcnf_file.name
                )

            plot_data = [(
                len(set(map(abs, acc_hard_tasks[0][1][0]))),
                len(acc_hard_tasks), len(acc_hard_tasks)
            )]
            for i, hard_tasks in enumerate(all_hard_tasks):
                next_acc_hard_tasks = []
                # split acc_hard_tasks instead offset and length params
                prod_size = len(acc_hard_tasks) * len(hard_tasks)
                for future in self.executor.submit_all(prod_worker, *((
                        self.problem, acc_part_hard_tasks, hard_tasks
                ) for acc_part_hard_tasks in slice_into(
                    acc_hard_tasks, self.executor.max_workers
                ))).as_complete():
                    prod_tasks, prod_time = future.result()
                    self.stats_sum['prod_time'] += prod_time
                    next_acc_hard_tasks.extend(prod_tasks)

                var_set = sorted(set(map(abs, next_acc_hard_tasks[0][1][0])))
                print(f'var set ({len(var_set)}):', ' '.join(map(str, var_set)))
                print('stats:', self.stats_sum)
                print(f'time ({self.executor.max_workers})',
                      now() - start_stamp)

                print(
                    f'reduced: {prod_size} -> {len(next_acc_hard_tasks)}',
                    f'({round(len(next_acc_hard_tasks) / prod_size, 2)})',
                )
                acc_hard_tasks = self.sifting(next_acc_hard_tasks)

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
            # print(self.best_model)
            print('parallel time:', now() - start_stamp)
            print('sequential time:', self.stats_sum['grow_time'] +
                  self.stats_sum['time'] + self.stats_sum['prod_time'])

            print('plot data')
            print(json.dumps(plot_data))

            [os.remove(file) for file in files]

        return self.stats_sum

        # filename = 'hard_tasks_prod.jsonl'
        # if self.logger._session is not None:
        #     filepath = self.logger._session.to_file(filename)
        #     with open(filepath, 'a+') as handle:
        #         for hard_task in acc_hard_tasks:
        #             string = json.dumps({
        #                 "assumptions": hard_task
        #             })
        #             handle.write(f'{string}\n')
        #
        # wght_hard_tasks = []
        # print('max weight:', sum(formula.wght))
        # print('best solution:', max_wght_solution)
        # with self.problem.solver.get_instance(formula.hard) as solver:
        #     for hard_task in acc_hard_tasks:
        #         penalty_weight = 0
        #         _, _, literals = solver.propagate((hard_task, []))
        #         value_map = {abs(lit): lit for lit in literals}
        #         for weight, clause in zip(formula.wght, formula.soft):
        #             if is_unsat(clause, value_map):
        #                 penalty_weight += weight
        #         wght_hard_tasks.append((penalty_weight, hard_task))
        #
        # acc_hard_tasks = sorted(wght_hard_tasks, key=lambda x: x[0])
        # print(acc_hard_tasks)
        #
        # future_all, i = self.executor.submit_all(hard_worker, *(
        #     (self.problem, hard_task) for _, hard_task in acc_hard_tasks
        # )), 0
        # while len(future_all) > 0:
        #     for future in future_all.as_complete(count=1):
        #         report = future.result()
        #         i, (status, _, model) = i + 1, report
        #         print(f'{i}/{len(acc_hard_tasks)}: {report}')
        #         tv = self.measure.check_and_get(report, self.budget)
        #         time_sum, value_sum = time_sum + tv[0], value_sum + tv[1]
        #
        #         if status:
        #             model_weight = calc_weight(formula, model)
        #             if max_wght_solution[0] < model_weight:
        #                 max_wght_solution = (model_weight, model)
        #                 print('best solution:', max_wght_solution)
        # 
        # result = {
        #     'value': time_sum,
        #     'time_sum': time_sum,
        #     'value_sum': value_sum,
        #     'real_time': now() - start_stamp,
        #     'hard_tasks': len(acc_hard_tasks),
        #     'total_tasks': 2 ** len(total_var_set)
        # }
        # self.logger._format(result, filename='result.jsonl')
        # return result

    def __config__(self) -> Dict[str, Any]:
        return {}


__all__ = [
    'CombineT'
]
