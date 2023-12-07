from time import time as now

from ...encoding import Clause
from ...variables import Supplements
from ...variables.vars import VarMap

from .pysat import PySatSetts, \
    _PySatSolver, PySatSolver
from ..solver import Report
from ...encoding import SatFormula


def is2clause(clause: Clause, var_map: VarMap) -> bool:
    size = len(clause)
    for literal in clause:
        var = abs(literal)
        value = var_map.get(var)
        if literal == value:
            return True
        if value is not None:
            size -= 1
    else:
        return size <= 2


class _Py2SatSolver(_PySatSolver):
    def __init__(
            self,
            formula: SatFormula,
            settings: PySatSetts,
            use_timer: bool = True,
            threshold: float = 1.0,
    ):
        super().__init__(formula, settings, use_timer)
        self.limit = (1 - threshold) * len(formula.clauses)

    def propagate(
            self, supplements: Supplements,
            ignore_constraints: bool = False
    ) -> Report:
        report = super().propagate(
            supplements, ignore_constraints
        )
        if report.status is not None: return report

        _, stats, literals, cost = report
        stamp, no2clause = now() - stats['time'], 0
        var_map = {abs(lit): lit for lit in literals}

        for clause in self.formula:
            no2clause += not is2clause(clause, var_map)
            if no2clause > self.limit: break
        else:
            stats['time'] = now() - stamp
            return Report(False, stats, literals, cost)

        stats['time'] = now() - stamp
        return Report(None, stats, literals, cost)


class Py2SatSolver(PySatSolver):
    slug = 'solver:py2sat'

    def __init__(self, threshold: float = 1.0, sat_name: str = 'm22'):
        super().__init__(sat_name=sat_name)
        self.threshold = threshold

    def get_instance(
            self, formula: SatFormula, use_timer: bool = True
    ) -> _Py2SatSolver:
        return _Py2SatSolver(formula, self.settings, use_timer)


__all__ = [
    'Py2SatSolver',
    '_Py2SatSolver',
]
