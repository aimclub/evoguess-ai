from typing import Dict, Any, Optional

from ..abc import Space
from ..model import Backdoor

from typings.searchable import Vector
from lib_satprob.variables import Variables


class BackdoorSet(Space):
    slug = 'space:backdoor_set'

    def __init__(
            self,
            variables: Variables,
            of_size: Optional[int] = None,
            by_string: Optional[str] = None,
            by_vector: Optional[Vector] = None,
            random_seed: Optional[int] = None,
    ):
        super().__init__(
            of_size,
            by_vector,
            random_seed
        )
        self.by_string = by_string
        self.variables = variables

    def get_initial(self) -> Backdoor:
        backdoor = self._get_searchable()
        if self.by_string is not None:
            var_names = self.by_string.split()
            backdoor._set_vector([
                1 if str(var) in var_names else
                0 for var in backdoor._variables
            ])

        size = len(self.variables)
        vector = self._get_vector(size)
        if vector is not None:
            backdoor._set_vector(vector)
        return backdoor

    # noinspection PyProtectedMember
    def get_by(self, vector: Vector) -> Backdoor:
        backdoor = self._get_searchable()
        backdoor._set_vector(vector)
        return backdoor

    # noinspection PyProtectedMember
    def _get_searchable(self) -> Backdoor:
        return Backdoor(variables=self.variables)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'of_size': self.of_size,
            'by_string': self.by_string,
            'by_vector': self.by_vector,
            'random_seed': self.random_seed,
            'variables': self.variables.__config__(),
        }


__all__ = [
    'BackdoorSet'
]
