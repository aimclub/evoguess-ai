from typing import NamedTuple, Optional, Dict

from instance.module.encoding import EncodingData
from function.module.budget import KeyLimit, UNLIMITED
from typings.searchable import Assumptions, Supplements, Constraints


class Report(NamedTuple):
    status: Optional[bool]
    stats: Dict[str, float]
    model: Optional[Assumptions]


class IncrSolver:
    def __init__(self, encoding_data: EncodingData, constraints: Constraints):
        self.encoding_data, self.constraints = encoding_data, constraints

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError

    def solve(self, assumptions: Assumptions,
              limit: KeyLimit = UNLIMITED,
              add_model: bool = False) -> Report:
        raise NotImplementedError

    def propagate(self, assumptions: Assumptions) -> Report:
        raise NotImplementedError


class Solver:
    slug = 'solver'

    def use_incremental(self, encoding_data: EncodingData,
                        constraints: Constraints = ()) -> IncrSolver:
        raise NotImplementedError

    def solve(self, encoding_data: EncodingData, supplements: Supplements,
              limit: KeyLimit = UNLIMITED, add_model: bool = False) -> Report:
        raise NotImplementedError

    def propagate(self, encoding_data: EncodingData, supplements: Supplements) -> Report:
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
    'KeyLimit',
    # const
    'UNLIMITED'
]
