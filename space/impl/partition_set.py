from typing import Dict, Any, Optional

from ..abc import Space

from typings.searchable import Vector
from ..model import Interval, Partition


class PartitionSet(Space):
    slug = 'space:partition_set'

    def __init__(
            self, length: int, interval: Interval,
            by_vector: Optional[Vector] = None
    ):
        super().__init__(by_vector)
        self.interval = interval
        self.length = length

    # noinspection PyProtectedMember
    def get_initial(self) -> Partition:
        interval = self._get_searchable()
        if self.by_vector is not None:
            interval._set_vector(self.by_vector)
        return interval

    def _get_searchable(self) -> Partition:
        return Partition(self.length, self.interval)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'length': self.length,
            'interval': self.interval.__config__(),
            'by_vector': self.by_vector,
        }


__all__ = [
    'PartitionSet'
]
