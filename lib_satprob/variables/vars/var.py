from typing import Any, List, Dict, Union

from .._utility import Assumptions, Supplements

AnyVar = Union['Var', int]
VarMap = Dict[AnyVar, int]


class Var:
    def __init__(self, dim: int, name: str):
        self.dim, self.name = dim, name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: 'Var'):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Var):
            return self.name == other.name
        else:
            return False

    def sub(self, value: int) -> Assumptions:
        raise NotImplementedError

    def substitute(self, var_map: VarMap) -> Supplements:
        raise NotImplementedError

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError

    @property
    def deps(self) -> List[AnyVar]:
        raise NotImplementedError


__all__ = [
    'Var',
    # types
    'AnyVar',
    'VarMap',
]
