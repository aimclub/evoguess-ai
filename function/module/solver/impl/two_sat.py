from time import time as now
from typing import Type, Dict
from pysat import solvers as slv, formula as fml

from ..solver import Report
from .pysat import IncrPySAT, PySAT
from ...budget import UNLIMITED, KeyLimit

from typings.searchable import Supplements, Assumptions, Constraints
from instance.module.encoding import Formula, Clause, Clauses


def is2clause(clause: Clause, value_map: Dict[int, int]) -> bool:
    index, size = 0, len(clause)
    while size > 2 and index < len(clause):
        literal = clause[index]
        value = value_map.get(abs(literal))
        if literal == value:
            return True
        if value is not None:
            size -= 1
        index += 1

    return size <= 2


def check(formula: Formula, threshold: float, report: Report) -> Report:
    if report.status: return report

    if isinstance(formula, fml.CNF):
        clauses = formula.clauses
    else:
        raise TypeError('PySat works only with CNF or CNF+ encodings')

    status, stats, literals = report
    value_map = {abs(lit): lit for lit in literals}
    false_count, false_limit = 0, (1 - threshold) * len(clauses)
    stamp, status = now() - stats['time'], False
    for clause in clauses:  # todo: constraints not supported
        false_count += not is2clause(clause, value_map)
        if false_count > false_limit: status = None

    stats['time'] = now() - stamp
    return Report(status, stats, literals)


class IncrTwoSAT(IncrPySAT):
    def __init__(self, formula: Formula, constraints: Constraints,
                 constructor: Type, threshold: float):
        super().__init__(formula, constraints, constructor)
        self.threshold = threshold

    def solve(self, assumptions: Assumptions,
              limit: KeyLimit = UNLIMITED,
              add_model: bool = False) -> Report:
        return self.propagate(assumptions)  # todo: maybe raise Exception?

    def propagate(self, assumptions: Assumptions) -> Report:
        return check(
            self.formula, self.threshold,
            super().propagate(assumptions)
        )


class TwoSAT(PySAT):
    slug = 'solver:two-sat'

    def __init__(self, threshold: float = 1.0):
        super().__init__(slv.Glucose3)
        # todo: move threshold to func
        self.threshold = threshold

    def use_incremental(self, formula: Formula,
                        constraints: Constraints = ()) -> IncrTwoSAT:
        return IncrTwoSAT(formula, constraints, self.constructor, self.threshold)

    def solve(self, formula: Formula, supplements: Supplements,
              limit: KeyLimit = UNLIMITED, add_model: bool = False) -> Report:
        return self.propagate(formula, supplements)

    def propagate(self, formula: Formula, supplements: Supplements) -> Report:
        report = super().propagate(formula, supplements)
        return check(formula, self.threshold, report)


__all__ = [
    'TwoSAT',
    # utils
    'is2clause'
]
