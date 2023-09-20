# import unittest
#
# from core.module.limitation import WallTime, Iteration
#
#
# class TestLimitation(unittest.TestCase):
#     def test_iteration(self):
#         limitation = Iteration(value=1000)
#         self.assertEqual(limitation.exhausted(), False)
#         self.assertEqual(limitation.left('time'), None)
#         self.assertEqual(limitation.left('iteration'), 1000)
#
#         limitation.increase('iteration', 990)
#         self.assertEqual(limitation.left('iteration'), 10)
#
#         limitation.set('iteration', 1234)
#         self.assertEqual(limitation.left('iteration'), 0)
#         self.assertEqual(limitation.get('iteration'), 1234)
#         self.assertEqual(limitation.exhausted(), True)
#
#     def test_wall_time(self):
#         limitation = WallTime(from_string='02:13:45')
#         self.assertEqual(limitation.exhausted(), False)
#         self.assertEqual(limitation.left('time'), 8025)
#         self.assertEqual(limitation.left('iteration'), None)
#
#         limitation.increase('time', 654)
#         self.assertEqual(limitation.get('time'), 654)
#         self.assertEqual(limitation.left('time'), 7371)
#
#         limitation.set('time', 10345)
#         self.assertEqual(limitation.left('time'), 0)
#         self.assertEqual(limitation.get('time'), 10345)
#         self.assertEqual(limitation.exhausted(), True)
