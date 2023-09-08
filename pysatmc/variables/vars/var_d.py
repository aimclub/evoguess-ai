from typing import Any, List, Dict

from .var import Var, AnyVar, VarMap
from ..._utility import Supplements


class Domain(Var):
    slug = 'var:domain'

    def __init__(self, name: str, group: List[int]):
        self.group = group
        super().__init__(len(group), name)

    def supplements(self, var_map: VarMap) -> Supplements:
        if self not in var_map:
            return [var if var_map[var] else -var for var in self.group], []
        else:
            return [var if var_map[self] == i else -var for i, var in
                    enumerate(self.group)], []

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'name': self.name,
            'group': self.group
        }

    @property
    def deps(self) -> List[AnyVar]:
        return [self]


__all__ = [
    'Domain'
]
