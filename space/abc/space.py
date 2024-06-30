from typing import Dict, Any, Optional
from numpy.random import RandomState, randint

from typings.searchable import Vector, ByteVector, Searchable


class Space:
    slug = 'space'

    def __init__(
            self,
            of_size: Optional[int] = None,
            by_vector: Optional[Vector] = None,
            random_seed: Optional[int] = None,
    ):
        self.of_size, self.by_vector = of_size, by_vector
        self.random_seed = random_seed or randint(2 ** 31)
        self.random_state = RandomState(seed=self.random_seed)

    @property
    def is_random_initial(self) -> bool:
        return not not self.of_size

    def get_initial(self) -> Searchable:
        raise NotImplementedError

    def _get_searchable(self) -> Searchable:
        raise NotImplementedError

    def unpack(self, byte_vec: ByteVector) -> Searchable:
        vector = Searchable.unpack(byte_vec)
        return self._get_searchable()._set_vector(vector)

    # noinspection PyProtectedMember
    def _get_vector(self, vector_size: int) -> Optional[Vector]:
        if self.by_vector is not None:
            return self.by_vector
        elif self.of_size is not None:
            nums = set(self.random_state.randint(
                0, vector_size, self.of_size
            ))
            return [
                1 if i in nums else 0
                for i in range(vector_size)
            ]

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError

    def __str__(self):
        return self.slug


__all__ = [
    'Space'
]
