from typing import Tuple

from ...models import Status
from typings.optional import Float, Str, Bool

STATUS_MAP = {
    False: Status.SOLVED,
    True: Status.RESOLVED,
    None: Status.INTERRUPTED,
}

Budget = Tuple[Str, Float]
EMPTY_BUDGET = ('', None)


class Measure:
    key = None
    slug = 'measure'

    def __init__(self,
                 budget: Float = None,
                 at_least: Float = None):
        self.budget = budget
        self.at_least = at_least

    def get_budget(self) -> Budget:
        return self.key, self.budget

    def check_and_get(self, stats, status: Bool) -> Tuple[Float, Status]:
        value = stats.get(self.key)
        if self.budget and status is None:
            return value, Status.EXHAUSTED
        if self.budget and value > self.budget:
            return value, Status.EXHAUSTED
        if self.at_least and value < self.at_least:
            return value, Status.NOT_REACHED
        return value, STATUS_MAP[status]

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'key': self.key,
            'slug': self.slug,
            'budget': self.budget,
            'at_least': self.at_least,
        }


__all__ = [
    'Measure',
    # types
    'Budget',
    # const
    'EMPTY_BUDGET',
]
