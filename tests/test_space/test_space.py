import unittest

from lib_satprob.variables import Indexes
from space.impl import BackdoorSet, IntervalSet


class TestSpace(unittest.TestCase):
    def test_backdoor_set(self):
        indexes = Indexes(from_iterable=[1, 2, 3, 4])

        # by_vector test set
        space = BackdoorSet(variables=indexes)
        backdoor = space.get_initial()
        for iv, bv in zip(indexes, backdoor):
            self.assertEqual(iv, bv)
        self.assertEqual(str(backdoor), '1 2 3 4')
        self.assertEqual(backdoor.get_vector(), [1, 1, 1, 1])

        space = BackdoorSet(variables=indexes, by_vector=[])
        backdoor = space.get_initial()
        self.assertEqual(str(backdoor), '')
        self.assertListEqual(backdoor.variables(), [])
        self.assertEqual(backdoor.get_vector(), [0, 0, 0, 0])

        space = BackdoorSet(variables=indexes, by_vector=[1, 0, 1])
        backdoor = space.get_initial()
        self.assertEqual(str(backdoor), '1 3')
        self.assertEqual(len(backdoor.variables()), 2)
        self.assertEqual(backdoor.get_vector(), [1, 0, 1, 0])

        # by_string test set
        space = BackdoorSet(variables=indexes, by_string='2 3')
        backdoor = space.get_initial()
        self.assertEqual(str(backdoor), '2 3')
        self.assertEqual(len(backdoor.variables()), 2)
        self.assertEqual(backdoor.get_vector(), [0, 1, 1, 0])

        space = BackdoorSet(variables=indexes, by_string='2 3 5')
        backdoor = space.get_initial()
        self.assertEqual(str(backdoor), '2 3')
        self.assertEqual(len(backdoor.variables()), 2)
        self.assertEqual(backdoor.get_vector(), [0, 1, 1, 0])

    def test_interval_set(self):
        indexes = Indexes(from_iterable=[1, 2, 3, 4])

        space = IntervalSet(indexes=indexes)
        interval = space.get_initial()
        self.assertEqual(repr(interval), '[0-1](16)')
        self.assertEqual(interval.get_vector(), [1, 1, 1, 1])

        space = IntervalSet(indexes=indexes, by_vector=[0, 1])
        interval = space.get_initial()
        self.assertEqual(repr(interval), '[0-3](5)')
        self.assertEqual(interval.get_vector(), [0, 1, 0, 0])
