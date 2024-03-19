import unittest

from numpy.random import randint

from utility.iterable import concat, to_oct, \
    to_bin, list_of, pick_by, omit_by, split_by


class TestUtils(unittest.TestCase):
    def test_utils(self):
        self.assertEqual(
            concat([1, 2, 3], [6, 7, 10]), [1, 2, 3, 6, 7, 10]
        )
        self.assertEqual(
            concat([1, 2], (4,), {5, 5, 5}, range(6, 8)), [1, 2, 4, 5, 6, 7]
        )

        self.assertEqual(to_oct(to_bin(57, 8)), 57)
        self.assertEqual(to_oct([1, 1, 1, 0, 0, 1]), 228)
        self.assertEqual(to_bin(45, 8), [0, 0, 1, 0, 1, 1, 0, 1])

        self.assertEqual(
            list_of(None, 103), [None] * 103
        )
        self.assertEqual(
            list_of(0, [1, 2, 3, 4, 5]), [0, 0, 0, 0, 0]
        )

        self.assertEqual(
            pick_by([1, 2, 3, 4], [0, 3, 6]), [1, 4]
        )
        self.assertEqual(
            pick_by([1, 2, 3, 4], lambda x: x > 3), [4]
        )
        self.assertEqual(
            pick_by(range(1000), [6, 80, 403]), [6, 80, 403]
        )
        self.assertEqual(
            pick_by(range(1000)[::-1], [6, 80, 403]), [993, 919, 596]
        )

        self.assertEqual(omit_by([1, 2, 3, 4], [1, 3, 6]), [1, 3])
        self.assertEqual(omit_by([1, 2, 3, 4], lambda x: x > 3), [1, 2, 3])

        for iterable, predicate in [
            (range(20), randint(0, 20, 9)),
            (range(1000), lambda x: x % 4 == 0),
            (range(1000), randint(0, 1000, 433)),
            (range(10000), randint(0, 10000, 4817))
        ]:
            self.assertEqual(
                split_by(iterable, predicate),
                (pick_by(iterable, predicate), omit_by(iterable, predicate))
            )
