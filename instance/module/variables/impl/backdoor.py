from ..variables import *

try:  # for python3.8 and greater
    from math import prod
except ImportError:  # for python3.7
    from operator import mul
    from functools import reduce


    def prod(_list):
        return reduce(mul, _list, 1)

from copy import copy
from itertools import compress
from util.iterable import concat, list_of, slice_by, to_oct, to_bin

Mask = List[int]
ByteMask = bytes


class Backdoor(Variables):
    slug = 'variables:backdoor'

    def __init__(self, from_file: str = None, from_vars: List[Var] = None):
        super().__init__(from_vars=from_vars, from_file=from_file)
        self._length = len(super().variables())
        self._mask = list_of(1, self._length)

        self._var_state = None

    def _upd_var_state(self):
        _variables = super().variables()
        self._var_state = list(compress(
            _variables, self._mask
        ))

    def variables(self) -> List[Var]:
        if not self._var_state:
            self._upd_var_state()
        return self._var_state

    def power(self) -> int:
        return prod(self.get_var_bases())

    def get_mask(self) -> List[int]:
        return copy(self._mask)

    def _set_mask(self, mask: Mask) -> 'Backdoor':
        if len(mask) > self._length:
            self._mask = mask[:self._length]
        else:
            dl = self._length - len(mask)
            self._mask = mask + list_of(0, dl)

        self._var_deps = None
        self._var_state = None
        self._var_bases = None
        self._deps_bases = None
        return self

    def get_copy(self, mask: Mask) -> 'Backdoor':
        return Backdoor(
            from_vars=self._vars,
            from_file=self.filepath,
        )._set_mask(mask)

    def pack(self) -> ByteMask:
        return bytes(map(to_oct, slice_by(self._mask, 8)))

    @staticmethod
    def unpack(bytemask: ByteMask) -> Mask:
        return concat(*(to_bin(number, 8) for number in bytemask))

    def __copy__(self):
        return self.get_copy(self._mask)


__all__ = [
    'Mask',
    'ByteMask',
    'Backdoor'
]
