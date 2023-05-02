from typing import Any, Callable, Dict, Tuple

from space import Space

from . import worker_t
from .worker_t import *

from ..module.solver.solver import Solver
from ..module.measure.measure import Measure

from typings.searchable import ByteVector
from instance.impl.instance import Instance

Payload = Tuple[
    Space,
    Solver,
    Measure,
    Instance,
    ByteVector
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
