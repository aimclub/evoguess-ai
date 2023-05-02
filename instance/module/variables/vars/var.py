from typing import Union, List, Dict, Any

from typings.searchable import Supplements

AnyVar = Union['Var', int]
VarMap = Dict[AnyVar, int]


class Var:
    def __init__(self, dim: int, name: str):
        self.dim = dim
        self.name = name

    @property
    def deps(self) -> List[AnyVar]:
        raise NotImplementedError

    def supplements(self, var_map: VarMap) -> Supplements:
        raise NotImplementedError

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Var):
            return self.name == other.name
        else:
            return False

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


__all__ = [
    'Var',
    # types
    'AnyVar',
    'VarMap'
]
