from time import time as now
from typing import Type, Dict
from pysat import solvers as pysat

from ..solver import Report
from .pysat import IncrPySAT, PySAT

from function.models import Status
from function.module.measure import Measure
from instance.module.encoding import EncodingData, CNFData, CNFPData, Clause
from instance.module.variables.vars import Supplements, Assumptions, Constraints


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


def check(data: EncodingData, threshold: float, report: Report, add_model: bool = True) -> Report:
    if not isinstance(data, CNFData) or isinstance(data, CNFPData):
        raise TypeError('TwoSAT works only with CNF encodings')
    if report.status == Status.RESOLVED:
        return report

    time, value, status, literals = report
    clauses, false_count = data.clauses(), 0
    false_limit = (1 - threshold) * len(clauses)
    value_map = {abs(lit): lit for lit in literals}
    stamp, model = now() - time, literals if add_model else None
    for clause in clauses:  # todo: constraints not supported
        false_count += not is2clause(clause, value_map)
        if false_count > false_limit:
            return Report(now() - stamp, value, Status.EXHAUSTED, model)
    return Report(now() - stamp, value, Status.SOLVED, model)


class IncrTwoSAT(IncrPySAT):
    def __init__(self, data: EncodingData, measure: Measure,
                 constructor: Type, constraints: Constraints, threshold: float):
        super().__init__(data, measure, constructor, constraints)
        self.threshold = threshold

    def solve(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        # todo: maybe raise Exception?
        return self.propagate(assumptions, add_model)

    def propagate(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        return check(self.data, self.threshold, super().propagate(assumptions), add_model)


class TwoSAT(PySAT):
    slug = 'solver:two-sat'

    def __init__(self, threshold: float = 1.0):
        super().__init__(pysat.Glucose3)
        # todo: move threshold to func
        self.threshold = threshold

    def solve(self, data: EncodingData, measure: Measure,
              supplements: Supplements, add_model: bool = True) -> Report:
        return self.propagate(data, measure, supplements, add_model)

    def propagate(self, data: EncodingData, measure: Measure,
                  supplements: Supplements, add_model: bool = True) -> Report:
        return check(data, self.threshold, super().propagate(data, measure, supplements), add_model)

    def use_incremental(self, data: EncodingData, measure: Measure,
                        constraints: Constraints = ()) -> IncrTwoSAT:
        return IncrTwoSAT(data, measure, self.constructor, constraints, self.threshold)


__all__ = [
    'TwoSAT',
    # utils
    'is2clause'
]
