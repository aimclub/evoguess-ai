from warnings import warn
from time import time as now
from typing import Dict, Any, Optional

from ..abc import Core
from output import Logger
from space.model import Backdoor

from lib_satprob.solver import Report
from lib_satprob.problem import Problem
from lib_satprob.derived import get_derived_by
from lib_satprob.encoding import is_sat_formula
from lib_satprob.variables import Supplements

from function.module.budget import TaskBudget
from function.module.measure import Measure


def warn_bad(backdoor: Backdoor):
    warn(f'Bad backdoor: {backdoor} (all tasks is hard!)')


class Solving(Core):
    slug = 'core:solving'

    def __init__(self, logger: Logger, problem: Problem,
                 budget: Optional[TaskBudget] = None,
                 measure: Optional[Measure] = None,
                 random_seed: Optional[int] = None):
        super().__init__(logger, problem, random_seed)
        self.budget, self.measure = budget, measure

    # todo: return iterator[report] instead of report
    def launch(self, *backdoors: Backdoor) -> Report:
        stamp, formula, = now(), self.problem.encoding.get_formula()
        assumptions_set, constraints_set, all_stats = set(), set(), {}

        def add_supplements(_supplements: Supplements):
            _assumptions, _constraints = _supplements
            assumptions_set.update(set(_assumptions))
            for _clause in map(tuple, _constraints):
                constraints_set.add(_clause)

        def get_report(_status, _stats, _model, _cost) -> Report:
            _stats = {**_stats, 'time': now() - stamp}
            return Report(_status, _stats, _model, _cost)

        print(f'Processing {len(backdoors)} passed backdoors...')
        with self.problem.solver.get_instance(formula, False) as solver:
            for backdoor, easy, hard in [(bd, [], []) for bd in backdoors]:
                for supplements in backdoor.enumerate():
                    status, stats, model, cost = solver.propagate(supplements)
                    (easy if status is False else hard).append(supplements)

                    if status is True and is_sat_formula(formula):
                        return get_report(status, stats, model, cost)

                if len(hard) == 0: return get_report(False, {}, None, None)
                warn_bad(backdoor) if len(easy) == 0 else add_supplements(
                    hard[0] if len(hard) == 1 else get_derived_by(easy)
                )

            a_len, c_len = len(assumptions_set), len(constraints_set)
            print(f'Derived {a_len} literals and {c_len} clauses')

            limit = self.measure.get_limit(self.budget) if \
                self.measure and self.budget else (None, None)
            status, stats, model, cost = solver.solve(([], [
                *([lit] for lit in assumptions_set),
                *(list(cl) for cl in constraints_set)
            ]), limit)
            return get_report(status, stats, model, cost)

    def __config__(self) -> Dict[str, Any]:
        return {}
