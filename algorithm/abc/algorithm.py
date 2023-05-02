from typing import List, Tuple, TYPE_CHECKING

from typings.optional import Int
from typings.searchable import Searchable

if TYPE_CHECKING:
    from core.model.point import Point, PointSet


# todo: move to a separate file
class PointManager:
    _vector = None
    _buffer = None

    def __init__(self, algorithm: 'Algorithm', point: 'Point'):
        self._algorithm = algorithm
        self._point = point
        self._index = 0

    def __enter__(self):
        self._vector = [self._point]
        self._buffer = []
        return self

    def solution(self) -> 'PointSet':
        return sorted(self._vector)

    def insert(self, *points: 'Point') -> Tuple[int, 'PointSet']:
        self._buffer.extend(points)
        if len(self._buffer) >= self._algorithm.min_update_size:
            self._vector = self._algorithm.update(self._vector, *self._buffer)
            self._index, self._buffer = self._index + 1, []
            return self._index, self._vector

    def collect(self, in_queue: int, available: int) -> List[Searchable]:
        if self._algorithm.max_queue_size is not None:
            max_queue_size = self._algorithm.max_queue_size
            available = max(0, max_queue_size - in_queue)
        return self._algorithm.next(self._vector, available)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._vector = None
        self._buffer = None


class Algorithm:
    slug = None

    def __init__(self, min_update_size: int, max_queue_size: Int):
        self.max_queue_size = max_queue_size
        self.min_update_size = min_update_size

    def start(self, point: 'Point') -> PointManager:
        return PointManager(self, point)

    def update(self, vector: 'PointSet', *points: 'Point') -> 'PointSet':
        raise NotImplementedError

    def next(self, vector: 'PointSet', count: int) -> List[Searchable]:
        raise NotImplementedError

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug,
        }
