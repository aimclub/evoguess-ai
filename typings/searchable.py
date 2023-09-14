from copy import copy
from typing import Optional, List, Dict, TypeVar, Any

from pysatmc.variables.vars import Var, VarMap
from pysatmc.variables import Supplements, Enumerable

from util.iterable import concat, list_of, slice_by, to_bin, to_oct

Vector = List[int]
ByteVector = bytes
TSearchable = TypeVar('TSearchable', bound='Searchable')


class Searchable(Enumerable):
    slug = 'searchable'

    def __init__(self, length: int):
        self._length = length
        self._vector = list_of(1, length)

    def power(self) -> int:
        raise NotImplementedError

    def dimension(self) -> List[int]:
        raise NotImplementedError

    def variables(self) -> List[Var]:
        raise NotImplementedError

    def substitute(self, using_values: Optional[List[int]] = None,
                   using_var_map: Optional[VarMap] = None) -> Supplements:
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


__all__ = [
    'Searchable',
    # types
    'Vector',
    'ByteVector',
    'Supplements',
]
