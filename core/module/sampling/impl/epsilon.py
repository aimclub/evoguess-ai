from math import sqrt, ceil
from typing import Dict, Any

from ..sampling import Sampling
from utility.iterable import concat
from function.model import Results


class Epsilon(Sampling):
    slug = 'sampling:epsilon'

    def __init__(self, step_size: int, epsilon: float,
                 max_size: int, split_into: int, delta: float = 0.05):
        super().__init__(max_size, split_into)
        self.step_size = step_size
        self.epsilon = step_size
        self.delta = delta

    def _get_epsilon(self, results: Results):
        values = concat(*[r.values.values() for r in results])
        size, expected = len(values), sum(values) / len(values)
        deviations = sum([(value - expected) ** 2 for value in values])
        return sqrt(deviations / (size - 1) / (self.delta * size)) / expected

    def summarize(self, results: Results) -> Dict[str, Any]:
        return {
            'epsilon': self._get_epsilon(results)
        }

    def get_count(self, offset: int, size: int, results: Results) -> int:
        if offset == 0:
            return min(self.step_size, size)
        elif offset < size and offset < self.max_size:
            if self._get_epsilon(results) > self.epsilon:
                count = min(offset + self.step_size, self.max_size, size)
                return max(0, count - offset)
        return 0

    @property
    def max_chunks(self) -> int:
        return ceil(self.step_size / self.split_into)

    def __config__(self):
        return {
            'slug': self.slug,
            'delta': self.delta,
            'epsilon': self.epsilon,
            'max_size': self.max_size,
            'step_size': self.step_size,
            'split_into': self.split_into
        }


__all__ = [
    'Epsilon'
]
