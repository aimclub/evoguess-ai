from typing import Any, Callable, Dict, Tuple, TYPE_CHECKING

from . import worker_t
from .worker_t import *

from ..module.solver.solver import Solver
from ..module.measure.measure import Measure

from instance.impl.instance import Instance
from instance.module.variables.impl.backdoor import ByteMask

if TYPE_CHECKING:
    from core.module.space import Space

Payload = Tuple[
    'Space',
    Solver,
    Measure,
    Instance,
    ByteMask
]

WorkerCallable = Callable[
    [WorkerArgs, Payload],
    WorkerResult
]

Estimation = Dict[str, Any]

__all__ = [
    'Payload',
    'Estimation',
    'WorkerCallable',
    *worker_t.__all__
]
