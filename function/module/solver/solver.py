from typing import NamedTuple, Any, Optional

from function.models import Status
from function.module.measure import Measure
from instance.module.encoding import EncodingData
from instance.module.variables.vars import Assumptions, Supplements, Constraints


class Report(NamedTuple):
    time: float
    value: float
    status: Status
    model: Optional[Any]


class IncrSolver:
    def __init__(self, data: EncodingData, measure: Measure):
        self.data, self.measure = data, measure

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError

    def solve(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        raise NotImplementedError

    def propagate(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        raise NotImplementedError


class Solver:
    slug = 'solver'

    def solve(self, data: EncodingData, measure: Measure,
              supplements: Supplements, add_model: bool) -> Report:
        raise NotImplementedError

    def propagate(self, data: EncodingData, measure: Measure,
                  supplements: Supplements, add_model: bool) -> Report:
        raise NotImplementedError

    def use_incremental(self, data: EncodingData, measure: Measure,
                        constraints: Constraints = ()) -> IncrSolver:
        raise NotImplementedError

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug
        }


__all__ = [
    'Solver',
    'IncrSolver',
    # types
    'Report',
]
