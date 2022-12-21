from typing import Optional, Union

Numeral = Union[int, float]


class Limitation:
    key = None
    slug = None

    def __init__(self, value: Numeral):
        self.limits = {
            'time': 0,
            'restarts': 0,
            'iteration': 0,
            'stagnation': 0
        }
        self.limit = value

    def exhausted(self) -> bool:
        return self.get(self.key) > self.limit

    def left(self, key: str) -> Optional[Numeral]:
        return None if self.key != key else \
            max(0, self.limit - self.get(key))

    def set(self, key: str, value: Numeral) -> Numeral:
        self.limits[key] = value
        return value

    def get(self, key: str, default: Numeral = 0) -> Numeral:
        return self.limits.get(key, default)

    def increase(self, key: str, value: Numeral = 1) -> Numeral:
        return self.set(key, self.limits[key] + value)

    def __str__(self):
        return self.slug


__all__ = [
    'Numeral',
    'Limitation'
]
