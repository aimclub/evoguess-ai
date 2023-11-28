import unittest
from copy import copy

from space.model import Interval

from lib_satprob.variables import Range, Indexes


class TestInterval(unittest.TestCase):
    def test_interval(self):
        interval = Interval(Range(start=1, length=64))
        self.assertEqual(interval.power(), 2 ** 64)
        self.assertEqual(len(interval), 0)

        interval_copy = copy(interval)
        self.assertEqual(interval.get_vector(), [1] * 64)
        self.assertEqual(interval.get_vector(), interval_copy.get_vector())

        tail_vector = [0] * 24 + interval.get_vector()[24:]
        interval_t40 = interval.make_copy(tail_vector)

        self.assertEqual(len(interval_t40), 24)
        self.assertEqual(str(interval_t40), f'0-{2 ** 24}')
        self.assertEqual(interval_t40._get_size(), (2 ** 24, 0))

        self.assertEqual(interval_t40.power(), 2 ** 40)
        self.assertEqual(repr(interval_t40), f'[0-{2 ** 24}]({2 ** 40})')

        self.assertEqual(interval_t40.get_vector(), [0] * 24 + [1] * 40)
        self.assertEqual(interval.get_vector(),
                         Interval.unpack(interval.pack()))

        head_vector = interval.get_vector()[:40] + [0] * 40
        interval_h40 = interval.make_copy(head_vector)

        self.assertEqual(len(interval_h40), 0)
        self.assertEqual(str(interval_h40), '0-1')
        self.assertEqual(interval_h40._get_size(), (1, 2 ** 24 - 1))

        self.assertEqual(interval_h40.power(), 2 ** 64 - 2 ** 24 + 1)
        self.assertEqual(repr(interval_h40), f'[0-1]({2 ** 64 - 2 ** 24 + 1})')

        self.assertEqual(interval_h40.get_vector(), [1] * 40 + [0] * 24)
        self.assertEqual(interval.get_vector(),
                         Interval.unpack(interval.pack()))

    def test_index_interval(self):
        str_iterable = '1 5 9 12 17 21 23 24 25 35'
        interval = Interval(Indexes(from_string=str_iterable))
        self.assertEqual(interval.power(), 2 ** 10)
        self.assertEqual(len(interval), 0)

        vector = [0, 0, 0, 1, 1, 0, 0, 1, 1, 1]
        interval = interval.make_copy(vector)
        self.assertEqual(interval.power(), 104)
        self.assertEqual(len(interval), 3)

        self.assertEqual(
            interval.substitute(using_values=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            ([-1, -5, -9, -12, -17, -21], [[-23, -24], [-23, -25]])
        )
        self.assertEqual(
            interval.substitute(using_values=[0, 1, 1, 0, 0, 1, 0, 1, 0, 1]),
            ([-1, 5, 9, -12, -17, 21], [[-23, -24], [-23, -25]])
        )
        self.assertEqual(
            interval.substitute(using_values=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            ([1, 5, 9, 12, 17, 21], [[23, 24], [23, 25], [23, 35]])
        )

        vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        interval = interval.make_copy(vector)
        self.assertEqual(interval.power(), 1)
        self.assertEqual(len(interval), 10)

        self.assertEqual(
            interval.substitute(using_values=[1, 1, 1, 1, 0, 0, 1, 1, 1, 1]),
            ([], [])
        )
