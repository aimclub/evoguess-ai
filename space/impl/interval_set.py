from typing import Dict, Any, Optional

from ..abc import Space
from ..model import Interval

from pysatmc.problem import Problem
from typings.searchable import Vector
from pysatmc.variables import Indexes


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
    def get_initial(self) -> Interval:
        interval = self._get_searchable()
        if self.by_vector is not None:
            interval._set_vector(self.by_vector)
        return interval

    def _get_searchable(self) -> Interval:
        return Interval(indexes=self.indexes)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'indexes': self.indexes.__config__(),
            'by_vector': self.by_vector,
        }


__all__ = [
    'IntervalSet'
]
