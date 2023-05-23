from typings.optional import Float
from ..budget import Budget


class TaskBudget(Budget):
    slug = 'budget:task'

    def __init__(self, value: Float):
        self._value = value

    def value(self) -> Float:
        return self._value


__all__ = [
    'TaskBudget'
]
