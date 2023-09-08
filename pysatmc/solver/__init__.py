from typing import Any, Dict, TypeVar

from .impl import *
from .solver import *
from . import impl, solver

impls = impl.solvers

TSolver = TypeVar('TSolver', bound='Solver')


def solver_from(config: Dict[str, Any]) -> TSolver:
    slug = config.pop('slug')
    return impls[slug](**config)


__all__ = [
    *impl.__all__,
    *solver.__all__,
    # from loader
    'solver_from',
]
