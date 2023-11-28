import json
from typing import List, Optional, Tuple

from output import Logger
from executor import Executor

from lib_satprob.solver import Report
from lib_satprob.problem import Problem
from typings.searchable import Searchable
from lib_satprob.variables import Assumptions, Supplements, combine
from util.iterable import split_by

from ..abc import Core

from function.module.measure import Measure
from function.module.budget import TaskBudget, KeyLimit


def is_sat(clause: List[int], solution: List[int]) -> bool:
    for literal in clause:
        if literal in solution:
            return True
    return False


def calc_weight(formula, solution: Assumptions) -> int:
    return sum([
        weight if is_sat(clause, solution) else 0 for
        weight, clause in zip(formula.wght, formula.soft)
    ])


def bool2sign(b):
    return -1 if b else 1


def signed(x, s):
    return bool2sign(s) * x


def minimize_dnf(dnf):
    from pyeda.inter import espresso_exprs

    print(f"Minimizing DNF via Espresso...")
    min_dnf = espresso_exprs(dnf)
    return min_dnf


def cnf_to_clauses(cnf):
    print("Converting CNF into clauses...")

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
    print(
        f"Total {len(clauses)} clauses: {sum(1 for clause in clauses if len(clause) == 1)} units, {sum(1 for clause in clauses if len(clause) == 2)} binary, {sum(1 for clause in clauses if len(clause) == 3)} ternary, {sum(1 for clause in clauses if len(clause) > 3)} larger"
    )
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


def propagate(
        problem: Problem, searchable: Searchable
) -> Tuple[List[Supplements], List[Supplements]]:
    up_tasks, no_up_tasks = [], []
    formula = problem.encoding.get_formula(copy=False)
    with problem.solver.get_instance(formula.hard) as solver:
        for supplements in searchable.enumerate():
            _, status, _, _ = solver.propagate(supplements)
            if status is None or status:
                no_up_tasks.append(supplements)
            else:
                up_tasks.append(supplements)

    return up_tasks, no_up_tasks


def limit_worker(
        problem: Problem, task: Supplements, limit: KeyLimit
) -> Tuple[Supplements, Report]:
    formula = problem.encoding.get_formula(copy=False)
    with problem.solver.get_instance(formula) as solver:
        weight, status, stats, model = solver.solve(task, limit)
        if status: weight = calc_weight(formula, model)
        return task, Report(weight, status, stats, model)


def grow(easy_tasks: List[Supplements]) -> Supplements:
    easy_cubes = [sups[0] for sups in easy_tasks]
    clauses = backdoor_to_clauses_via_easy(easy_cubes)
    const, one_lit = split_by(clauses, lambda x: len(x) > 1)
    return [clause[0] for clause in one_lit], const


class GrowingT(Core):
    slug = 'core:growing'

    def __init__(self, logger: Logger, measure: Measure, problem: Problem,
                 executor: Executor, budget: TaskBudget,
                 random_seed: Optional[int] = None):
        self.budget = budget
        self.measure = measure
        self.executor = executor
        super().__init__(logger, problem, random_seed)

        self.stats_sum = {}
        self.max_weight = None
        self.best_model = (0, [])

    def sifting(self, tasks: List[Supplements]) -> List[Supplements]:
        easy_tasks, limit = [], self.measure.get_limit(self.budget)
        future_all, count = self.executor.submit_all(limit_worker, *(
            (self.problem, task, limit) for task in tasks
        )), len(tasks)

        while len(future_all) > 0:
            for future in future_all.as_complete(count=1):
                task, report = future.result()
                for key, value in report.stats.items():
                    self.stats_sum[key] = \
                        self.stats_sum.get(key, 0.) + value

                if report.status is False: easy_tasks.append(task)
                if report.cost and report.cost > self.best_model[0]:
                    self.best_model = (report.cost, report.model)
                print(f'{count - len(future_all)}/{count}: {report}')

        return easy_tasks

    def launch(self, *searchables: Searchable) -> Report:
        formula = self.problem.encoding.get_formula(copy=False)
        self.max_weight, grown_sups = sum(formula.wght), []

        # start load formula cache
        # ---------------------------------
        filepath = self.problem.encoding.from_file
        filename = filepath and filepath.split('/')[-1]
        try:
            with open('growing-cache.json') as handle:
                growing_cache = json.load(handle)
        except FileNotFoundError:
            growing_cache = {}

        limit = str(self.measure.get_limit(self.budget))
        if filename and (filename in growing_cache):
            formula_cache = growing_cache[filename]
            limit_cache = formula_cache.get(limit, {})
        else:
            formula_cache, limit_cache = {}, {}
        # ---------------------------------
        # end load formula cache

        print(len(limit_cache))
        uniq_assumptions, uniq_constraints = set(), set()
        for index, searchable in enumerate(searchables):
            if str(searchable) not in limit_cache:
                easy, hard = propagate(self.problem, searchable)
                grow_clauses = grow([*easy, *self.sifting(hard)])
                limit_cache[str(searchable)] = grow_clauses

            if filename is not None:
                with open('growing-cache.json', 'w+') as handle:
                    json.dump({
                        **growing_cache,
                        filename: {
                            **formula_cache,
                            limit: limit_cache
                        }
                    }, handle)

            grown_sups.append(limit_cache[str(searchable)])

        for assumptions, constraints in grown_sups:
            uniq_assumptions.update(assumptions)
            uniq_constraints.update([
                tuple(sorted(constraint, key=abs))
                for constraint in constraints
            ])

        if filename is not None:
            filename = filename.split('.')[0]
            _formula = self.problem.encoding.get_formula()
            _formula.extend(list(uniq_constraints) + [
                [lit] for lit in uniq_assumptions
            ])
            _formula.to_file(f'{filename}_{len(searchables)}.wcnf')

        print('one lit:', len(uniq_assumptions))
        print('clauses:', len(uniq_constraints))

        print('max weight:', self.max_weight)
        print('best solution:', self.best_model)
        return self.problem.solver.solve(formula, (
            list(uniq_assumptions), list(map(list, uniq_constraints))
        ))


__all__ = [
    'GrowingT'
]
