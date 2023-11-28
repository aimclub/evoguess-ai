import unittest

from space.model import Backdoor
from lib_satprob.variables import Range

from core.model.point import Point
from core.module.comparator import MinValueMaxSize

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
        backdoor = Backdoor(Range(start=1, length=8))
        vector = [
            Point(backdoor.make_copy([]), comparator).set(value=1000),
            Point(backdoor.make_copy([0, 0, 1]), comparator).set(value=900),
            Point(backdoor.make_copy([1, 1, 1]), comparator).set(value=700),
            Point(backdoor.make_copy([0, 1, 1]), comparator).set(value=800),
            Point(backdoor.make_copy([0, 1, 1, 1]), comparator).set(value=650),
        ]

        selection = BestPoint(best_count=1)
        self.assertEqual(selection.select(vector, 3), [vector[4]] * 3)

        selection = BestPoint(best_count=2)
        selection.random_state = RandomStateStub([0, 1])
        self.assertEqual(selection.select(vector, 2), [vector[4], vector[2]])

        selection = BestPoint(best_count=2)
        self.assertEqual(
            selection.select([vector[0]], 2), [vector[0], vector[0]]
        )

    def test_roulette(self):
        comparator = MinValueMaxSize()
        backdoor = Backdoor(Range(start=1, length=8))
        vector = [
            Point(backdoor.make_copy([]), comparator).set(value=3000),
            Point(backdoor.make_copy([0, 0, 1]), comparator).set(value=1000),
            Point(backdoor.make_copy([1, 1, 1]), comparator).set(value=2000),
            Point(backdoor.make_copy([0, 1, 1]), comparator).set(value=2000),
            Point(backdoor.make_copy([0, 1, 1, 1]), comparator).set(value=1000),
        ]

        selection = Roulette()
        selection.random_state = RandomStateStub([0.05, 0.8])
        self.assertEqual(
            selection.select(vector, 2), [vector[0], vector[4]]
        )

        selection = Roulette()
        selection.random_state = RandomStateStub([0.05, 0.05, 0.8, 0.65])
        self.assertEqual(
            selection.select(vector, 4),
            [vector[0], vector[0], vector[4], vector[3]]
        )
