from typing import Dict, Any, Optional

from ..abc import Space
from ..model import Interval

from instance import Instance
from typings.searchable import Vector
from instance.module.variables import Indexes


class IntervalSet(Space):
    slug = 'space:interval_set'

    def __init__(
            self,
            indexes: Indexes,
            by_vector: Optional[Vector] = None
    ):
        super().__init__(by_vector)
        self.indexes = indexes

    # noinspection PyProtectedMember
    def get_initial(self, instance: Instance) -> Interval:
        interval = self._get_searchable(instance)
        if self.by_vector is not None:
            interval._set_vector(self.by_vector)
        return interval

    def _get_searchable(self, instance: Instance) -> Interval:
        return Interval(indexes=self.indexes)

    def __config__(self) -> Dict[str, Any]:
        pass


__all__ = [
    'IntervalSet'
]
