from typing import Tuple

from function.model import Status
from pysatmc.solver import Report
from function.module.budget import Budget, KeyLimit, UNLIMITED

from typings.optional import Float

STATUS_MAP = {
    False: Status.SOLVED,
    True: Status.RESOLVED,
    None: Status.INTERRUPTED,
}


class Measure:
    key = None
    slug = 'measure'

    def __init__(self, at_least: Float = None):
        self.at_least = at_least

    def get_limit(self, budget: Budget) -> KeyLimit:
        value = budget.value()
        return (self.key, value) if value else UNLIMITED

    def check_and_get(self, report: Report, budget: Budget) -> Tuple[Float, Float, Status]:
        time = report.stats.get('time')
        value = report.stats.get(self.key)

        budget_value = budget.value()
        if budget_value and report.status is None:
            return time, value, Status.EXHAUSTED
        if budget_value and value > budget_value:
            return time, value, Status.EXHAUSTED
        if self.at_least and value < self.at_least:
            return time, value, Status.NOT_REACHED
        return time, value, STATUS_MAP[report.status]

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'key': self.key,
            'slug': self.slug,
            'at_least': self.at_least,
        }


__all__ = [
    'Measure',
    # types
    'Budget',
]
