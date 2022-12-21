class Ordered:
    def __init__(self, comparator):
        self.comparator = comparator

    def compare(self, other):
        return self.comparator.compare(self, other)

    def __lt__(self, other):
        return self.compare(other) < 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __ge__(self, other):
        return self.compare(other) >= 0
