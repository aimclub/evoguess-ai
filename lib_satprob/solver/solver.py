from typing import Any, List, Dict, Tuple, Optional, NamedTuple

from ..variables import Supplements
from ..encoding.patch import SatPatch

KeyLimit = Tuple[
    Optional[str],
    Optional[float]
]

UNLIMITED = (None, None)


class Report(NamedTuple):
    status: Optional[bool]
    stats: Dict[str, float]
    model: Optional[List[Any]]
    cost: Optional[int] = None


class _Solver:
    def __init__(
            self, formula: Any,
            use_timer: bool = True
    ):
        self.formula = formula
        self.use_timer = use_timer

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, *args):
        raise NotImplementedError

    def solve(
            self,
            supplements: Supplements,
            limit: KeyLimit = UNLIMITED,
            extract_model: bool = True
    ) -> Report:
        raise NotImplementedError

    def propagate(
            self,
            supplements: Supplements
    ) -> Report:
        raise NotImplementedError

    def apply(
            self,
            patch: SatPatch
    ) -> '_Solver':
        raise NotImplementedError


class Solver:
    def get_instance(
            self, formula: Any,
            use_timer: bool = True
    ) -> _Solver:
        raise NotImplementedError

    def solve(
            self, formula: Any,
            supplements: Supplements,
            limit: KeyLimit = UNLIMITED,
            extract_model: bool = True,
            use_timer: bool = True
    ) -> Report:
        with self.get_instance(formula, use_timer) as solver:
            return solver.solve(supplements, limit, extract_model)

    def propagate(
            self, formula: Any,
            supplements: Supplements,
            use_timer: bool = True
    ) -> Report:
        with self.get_instance(formula, use_timer) as solver:
            return solver.propagate(supplements)

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


__all__ = [
    'Solver',
    '_Solver',
    # types
    'Report',
    'KeyLimit',
    # const
    'UNLIMITED'
]
