import unittest

from core.model.point import Point
from core.module.comparator import MinValueMaxSize
from instance.module.variables import Backdoor, Interval
from algorithm.module.selection import BestPoint, Roulette


class RandomStateStub:
    def __init__(self, values):
        self.values = values

    def rand(self, *args):
        return self.values

    def permutation(self, *args):
        return self.values


class TestSelection(unittest.TestCase):
    def test_best_point(self):
        comparator = MinValueMaxSize()
        backdoor = Backdoor(
            from_vars=Interval(start=1, length=8).variables()
        )
        vector = [
            Point(backdoor.get_copy([]), comparator).set(value=1000),
            Point(backdoor.get_copy([0, 0, 1]), comparator).set(value=900),
            Point(backdoor.get_copy([1, 1, 1]), comparator).set(value=700),
            Point(backdoor.get_copy([0, 1, 1]), comparator).set(value=800),
            Point(backdoor.get_copy([0, 1, 1, 1]), comparator).set(value=650),
        ]

        selection = BestPoint(best_count=1)
        self.assertEqual(selection.select(vector, 3), [vector[4]] * 3)

        selection = BestPoint(best_count=2)
        selection.random_state = RandomStateStub([0, 1])
        self.assertEqual(selection.select(vector, 2), [vector[4], vector[2]])

        selection = BestPoint(best_count=2)
        self.assertEqual(selection.select([vector[0]], 2), [vector[0], vector[0]])
        # selection.select(vector, 3)

    def test_roulette(self):
        comparator = MinValueMaxSize()
        backdoor = Backdoor(
            from_vars=Interval(start=1, length=8).variables()
        )
        vector = [
            Point(backdoor.get_copy([]), comparator).set(value=3000),
            Point(backdoor.get_copy([0, 0, 1]), comparator).set(value=1000),
            Point(backdoor.get_copy([1, 1, 1]), comparator).set(value=2000),
            Point(backdoor.get_copy([0, 1, 1]), comparator).set(value=2000),
            Point(backdoor.get_copy([0, 1, 1, 1]), comparator).set(value=1000),
        ]

        selection = Roulette()
        selection.random_state = RandomStateStub([0.05, 0.8])
        self.assertEqual(selection.select(vector, 2), [vector[0], vector[4]])

        selection = Roulette()
        selection.random_state = RandomStateStub([0.05, 0.05, 0.8, 0.65])
        self.assertEqual(selection.select(vector, 4), [vector[0], vector[0], vector[4], vector[3]])
