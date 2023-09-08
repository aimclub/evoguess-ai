from typing import Any, Dict, List, Callable

from .var import Var, AnyVar, VarMap
from ..._utility import Supplements, to_bin


class Switch(Var):
    slug = 'var:switch'

    def __init__(self, name: str, group: List[int], fn: Callable):
        self.group, self.fn = group, fn
        super().__init__(2, name)

    def supplements(self, var_map: VarMap) -> Supplements:
        constraints, size = [], len(self.group)
        value = var_map[self] if self in var_map else \
            self.fn(*(var_map[i] for i in self.group))
        for number in range(0, 2 ** size):
            bits = to_bin(number, size)
            if self.fn(*bits) != value:
                constraints.append([
                    -var if bit else var for
                    var, bit in zip(self.group, bits)
                ])
        return [], constraints

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'name': self.name,
            'group': self.group,
        }

    @property
    def deps(self) -> List[AnyVar]:
        return self.group


def xor(*args: bool) -> bool:
    return sum(args) % 2 == 1


class XorSwitch(Switch):
    slug = 'var:switch:xor'

    def __init__(self, name: str, group: List[int]):
        super().__init__(name, group, xor)


def bent4(x1: bool, x2: bool, x3: bool, x4: bool) -> bool:
    return xor(x1 and x3, x2 and x4)


class Bent4Switch(Switch):
    slug = 'var:switch:bent4'

    def __init__(self, name: str, group: List[int]):
        assert len(group) == 4
        super().__init__(name, group, bent4)


def majority(*args: bool) -> bool:
    return sum(args) > len(args) // 2


class MajoritySwitch(Switch):
    slug = 'var:switch:majority'

    def __init__(self, name: str, group: List[int]):
        super().__init__(name, group, majority)


__all__ = [
    'Switch',
    'XorSwitch',
    'Bent4Switch',
    'MajoritySwitch',
    # operations
    'majority',
    'bent4',
    'xor',
]
