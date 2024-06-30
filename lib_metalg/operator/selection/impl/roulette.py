from typing import List

from core.model.point import Point
from ..selection import *


class Roulette(Selection):
    slug = 'selection:roulette'

    def select(self, population: List[Point], size: int) -> List[Point]:
        ranges, rng, count = [], 0, len(population)
        for i, point1 in enumerate(population):
            w = 0.
            for point2 in population:
                w += point1.value() / point2.value()
            rng = rng + (1. / w) if (i != count - 1) else 1.
            ranges.append(rng)

        def get(prob):
            for k in range(0, count):
                if ranges[k] >= prob:
                    return population[k]
            return population[-1]

        return [get(p) for p in self.random_state.rand(size)]


__all__ = [
    'Roulette'
]
