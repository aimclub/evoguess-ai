class Ordered:
    def __init__(self, comparator):
        self.comparator = comparator

    def __lt__(self, other):
        return self.comparator.compare(self, other) < 0

    def __le__(self, other):
        return self.comparator.compare(self, other) <= 0

    def __eq__(self, other):
        return self.comparator.compare(self, other) == 0

    def __ge__(self, other):
        return self.comparator.compare(self, other) >= 0

    def __gt__(self, other):
        return self.comparator.compare(self, other) > 0


__all__ = [
    'Ordered'
]
