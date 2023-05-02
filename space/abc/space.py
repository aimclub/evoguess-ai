from typing import Dict, Any, Optional

from instance import Instance
from typings.searchable import Vector, ByteVector, Searchable


class Space:
    slug = 'space'

    def __init__(self, by_vector: Optional[Vector] = None):
        self.by_vector = by_vector

    def get_initial(self, instance: Instance) -> Searchable:
        raise NotImplementedError

    def _get_searchable(self, instance: Instance) -> Searchable:
        raise NotImplementedError

    # noinspection PyProtectedMember
    def unpack(self, instance: Instance, byte_vec: ByteVector) -> Searchable:
        searchable = self._get_searchable(instance)
        return searchable._set_vector(Searchable.unpack(byte_vec))

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError

    def __str__(self):
        return self.slug


__all__ = [
    'Space'
]
