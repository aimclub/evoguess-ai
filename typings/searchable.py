from copy import copy
from typing import Optional, Tuple, List, Dict, TypeVar, TYPE_CHECKING, Any

from util.iterable import concat, list_of, slice_by, to_bin, to_oct

if TYPE_CHECKING:
    from instance.module.variables.vars import Var

Vector = List[int]
ByteVector = bytes
TSearchable = TypeVar('TSearchable', bound='Searchable')

Assumptions = List[int]
Constraints = List[List[int]]
Supplements = Tuple[Assumptions, Constraints]


class Searchable:
    slug = 'searchable'

    def __init__(self, length: int):
        self._length = length
        self._vector = list_of(1, length)

    def power(self) -> int:
        raise NotImplementedError

    def dimension(self) -> List[int]:
        raise NotImplementedError

    def dependents(self) -> List['Var']:
        raise NotImplementedError

    def substitute(
            self,
            with_var_map: Optional[Dict[int, bool]] = None,
            with_substitution: Optional[List[bool]] = None,
    ) -> Supplements:
        raise NotImplementedError

    def get_vector(self) -> Vector:
        return copy(self._vector)

    def make_copy(self, vector: Vector) -> TSearchable:
        return copy(self)._set_vector(vector)

    def _set_vector(self, vector: Vector) -> TSearchable:
        if len(vector) > self._length:
            self._vector = vector[:self._length]
        else:
            dl = self._length - len(vector)
            self._vector = vector + list_of(0, dl)
        return self

    def pack(self) -> ByteVector:
        return bytes(map(to_oct, slice_by(self.get_vector(), 8)))

    @staticmethod
    def unpack(byte_vec: ByteVector) -> Vector:
        return concat(*(to_bin(number, 8) for number in byte_vec))

    def __len__(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __copy__(self) -> TSearchable:
        raise NotImplementedError

    def __eq__(self, other: TSearchable) -> bool:
        raise NotImplementedError

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


def combine(*args: Supplements) -> Supplements:
    assumptions, constraints = [], []
    for supplements in args:
        assumptions.extend(supplements[0])
        constraints.extend(supplements[1])
    return assumptions, constraints


__all__ = [
    'Searchable',
    # types
    'Vector',
    'ByteVector',
    'Assumptions',
    'Constraints',
    'Supplements',
    # tools
    'combine'
]
