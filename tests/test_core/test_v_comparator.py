# import unittest
#
# from space.model import Backdoor
# from pysatmc.variables import Range
#
# from core.model.point import Point
# from core.module.comparator import MinValueMaxSize
#
#
# class TestComparator(unittest.TestCase):
#     def test_min_value_max_size(self):
#         comparator = MinValueMaxSize()
#         backdoor = Backdoor(Range(start=1, length=8))
#         self.assertGreater(
#             Point(backdoor.make_copy([]), comparator).set(value=1000),
#             Point(backdoor.make_copy([0, 0, 1]), comparator).set(value=900),
#         )
#         self.assertGreater(
#             Point(backdoor.make_copy([0, 0, 1]), comparator).set(value=1000),
#             Point(backdoor.make_copy([1, 1, 1]), comparator).set(value=1000),
#         )
#         self.assertEqual(
#             Point(backdoor.make_copy([0, 1, 1]), comparator).set(value=1000),
#             Point(backdoor.make_copy([1, 0, 1]), comparator).set(value=1000),
#         )
#         self.assertLess(
#             Point(backdoor.make_copy([0, 1, 1]), comparator).set(value=1000),
#             Point(backdoor.make_copy([0, 0, 1]), comparator).set(value=1000),
#         )
#         self.assertLess(
#             Point(backdoor.make_copy([0, 1, 1]), comparator).set(value=1000),
#             Point(backdoor.make_copy([1, 0, 1]), comparator).set(value=float('inf')),
#         )
