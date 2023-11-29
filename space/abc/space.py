from typing import Dict, Any, Optional

from typings.searchable import Vector, ByteVector, Searchable


class Space:
    slug = 'space'

    def __init__(self, by_vector: Optional[Vector] = None):
        self.by_vector = by_vector

    def get_initial(self) -> Searchable:
        raise NotImplementedError

    def _get_searchable(self) -> Searchable:
        raise NotImplementedError

    # noinspection PyProtectedMember
    def unpack(self, byte_vec: ByteVector) -> Searchable:
        vector = Searchable.unpack(byte_vec)
        return self._get_searchable()._set_vector(vector)

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError

    def __str__(self):
        return self.slug


__all__ = [
    'Space'
]
