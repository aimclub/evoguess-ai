from time import time
from typing import Union, Optional

Numeral = Union[int, float]


class Stats:
    def __init__(self):
        self._stats = {}

    def __str__(self) -> str:
        return str({key: value for key, value in [
            ('time', time() - v) if k == 'stamp' else
            (k, v) for k, v in self._stats.items()
        ]})

    def get(self, key: str, default: Numeral = 0) -> Numeral:
        if key == 'time' and 'stamp' in self._stats:
            return time() - self._stats['stamp']
        else: return self._stats.get(key, default)

    def set(self, key: str, value: Numeral) -> Numeral:
        self._stats[key] = value
        return value

    def increase(self, key: str, value: Numeral = 1) -> Numeral:
        return self.set(key, self.get(key) + value)


class Condition:
    key = None

    def __init__(self, limit: Numeral):
        self._limit = self._step = limit

    def move(self, stats: Stats):
        self._limit = stats.get(self.key) + self._step

    def reached(self, stats: Stats) -> bool:
        return stats.get(self.key, -1) >= self._limit

    def left(self, stats: Stats) -> Optional[Numeral]:
        return None if self.key != 'time' else \
            max(0, self._limit - stats.get('time'))


class IterCond(Condition):
    key = 'iter'


class TimeCond(Condition):
    key = 'time'


class EmptyCond(Condition):
    def __init__(self):
        super().__init__(0)


__all__ = [
    'IterCond',
    'TimeCond',
    'Condition',
    # stub
    'EmptyCond',
    # types
    'Stats'
]
