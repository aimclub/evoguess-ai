from typing import Dict, Any
from time import time as now

from ..abc import Core

from space.model import Backdoor
from lib_satprob.solver import Report
from lib_satprob.derived import get_derived_by
from lib_satprob.variables import Supplements


class Solving(Core):
    slug = 'core:solving'

    def launch(self, *backdoors: Backdoor) -> Report:
        stamp, formula, = now(), self.problem.encoding.get_formula()
        assumptions_set, constraints_set, all_stats = set(), set(), {}

        def add_supplements(_supplements: Supplements):
            _assumptions, _constraints = _supplements
            assumptions_set.update(set(_assumptions))
            for _clause in map(tuple, _constraints):
                constraints_set.add(_clause)

        def get_report(_status, _stats, _model) -> Report:
            _time = _stats.get('time', 0.) + now() - stamp
            return Report(_status, {'time': _time}, _model)

        with self.problem.solver.get_instance(formula) as solver:
            for backdoor, easy, hard in [(bd, [], []) for bd in backdoors]:
                for supplements in backdoor.enumerate():
                    status, stats, model, _ = solver.propagate(supplements)
                    (easy if status is False else hard).append(supplements)
                    if status is True: return get_report(status, {}, model)

                if len(hard) == 0: return get_report(False, {}, None)
                add_supplements(
                    hard[0] if len(hard) == 1 else get_derived_by(easy)
                )

            assumptions = list(assumptions_set)
            constraints = [list(c) for c in constraints_set]
            report = solver.solve((assumptions, constraints))
            return get_report(report.status, report.stats, report.model)

    def __config__(self) -> Dict[str, Any]:
        return {}
