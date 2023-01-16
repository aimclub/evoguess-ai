import unittest

from core.model.point import Point
from core.module.comparator import MinValueMaxSize
from instance.module.variables import Interval, make_backdoor


class TestComparator(unittest.TestCase):
    def test_min_value_max_size(self):
        comparator = MinValueMaxSize()
        backdoor = make_backdoor(Interval(start=1, length=8))
        self.assertGreater(
            Point(backdoor.get_copy([]), comparator).set(value=1000),
            Point(backdoor.get_copy([0, 0, 1]), comparator).set(value=900),
        )
        self.assertGreater(
            Point(backdoor.get_copy([0, 0, 1]), comparator).set(value=1000),
            Point(backdoor.get_copy([1, 1, 1]), comparator).set(value=1000),
        )
        self.assertEqual(
            Point(backdoor.get_copy([0, 1, 1]), comparator).set(value=1000),
            Point(backdoor.get_copy([1, 0, 1]), comparator).set(value=1000),
        )
        self.assertLess(
            Point(backdoor.get_copy([0, 1, 1]), comparator).set(value=1000),
            Point(backdoor.get_copy([0, 0, 1]), comparator).set(value=1000),
        )
        self.assertLess(
            Point(backdoor.get_copy([0, 1, 1]), comparator).set(value=1000),
            Point(backdoor.get_copy([1, 0, 1]), comparator).set(value=float('inf')),
        )
