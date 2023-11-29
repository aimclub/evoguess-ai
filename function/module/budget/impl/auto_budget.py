from enum import Enum

from ..budget import Budget
# from typings.searchable import Searchable


class AutoMode(Enum):
    [
        Soft,
        Hard,
        Ignore
    ] = range(3)


class AutoBudget(Budget):
    slug = 'budget:auto'
    _value = None
    _power = None

    def __init__(self, mode: AutoMode = AutoMode.Ignore):
        self.mode = mode

    # def fit(self, searchable: Searchable) -> 'AutoBudget':
    #     if self._value and self._power:
    #         budget = AutoBudget(mode=self.mode)
    #         scale = self._power / searchable.power()
    #         budget._value = self._value * scale
    #         budget._power = searchable.power()
    #         return budget
    #     else:
    #         return self
    #
    # def set(self, value: float, power: float):
    #     self._value, self._power = value, power

    def value(self) -> float:
        return 0


__all__ = [
    'AutoBudget',
    # types
    'AutoMode'
]
