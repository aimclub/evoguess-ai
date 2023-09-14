from typing import Dict, Any, Optional

from ..abc import Space
from ..model import Backdoor

from pysatmc.problem import Problem
from typings.searchable import Vector
from pysatmc.variables import Variables


class BackdoorSet(Space):
    slug = 'space:backdoor_set'

    def __init__(
            self,
            variables: Variables,
            by_string: Optional[str] = None,
            by_vector: Optional[Vector] = None
    ):
        super().__init__(by_vector)
        self.by_string = by_string
        self.variables = variables

    # noinspection PyProtectedMember
    def get_initial(self, problem: Problem) -> Backdoor:
        backdoor = self._get_searchable(problem)
        if self.by_string is not None:
            var_names = self.by_string.split()
            backdoor._set_vector([
                1 if str(var) in var_names else
                0 for var in backdoor._variables
            ])
        elif self.by_vector is not None:
            backdoor._set_vector(self.by_vector)
        return backdoor

    def _get_searchable(self, problem: Problem) -> Backdoor:
        return Backdoor(variables=self.variables)

    def __config__(self) -> Dict[str, Any]:
        # todo: add realisation
        pass


__all__ = [
    'BackdoorSet'
]
