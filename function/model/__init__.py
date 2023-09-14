from typing import Any, Callable, Dict, Tuple

from space import Space
from pysatmc.problem import Problem

from . import worker_t
from .worker_t import *

from ..module.budget.budget import Budget
from ..module.measure.measure import Measure

from typings.searchable import ByteVector

Payload = Tuple[
    Space,
    Budget,
    Measure,
    Problem,
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
