import unittest

from function.models import Status
from function.module.measure import SolvingTime, Propagations, Conflicts, LearnedLiterals


class TestMeasure(unittest.TestCase):
    def test_solving_time(self):
        measure = SolvingTime()
        self.assertEqual(measure.get_budget(), ('time', None))
        self.assertEqual(measure.check_and_get(
            {'time': 56}, True), (56, Status.RESOLVED)
        )
        self.assertEqual(measure.check_and_get(
            {'time': 3.2}, None), (3.2, Status.INTERRUPTED)
        )
        self.assertEqual(measure.check_and_get(
            {'conflicts': 43}, False), (None, Status.SOLVED)
        )

        measure = SolvingTime(budget=6.5, at_least=3.2)
        self.assertEqual(measure.get_budget(), ('time', 6.5))
        self.assertEqual(measure.check_and_get(
            {'time': 6.6}, None), (6.6, Status.EXHAUSTED)
        )
        self.assertEqual(measure.check_and_get(
            {'time': 3.1}, True), (3.1, Status.NOT_REACHED)
        )

    def test_conflicts(self):
        measure = Conflicts(budget=10000)
        self.assertEqual(measure.get_budget(), ('conflicts', 10000))
        self.assertEqual(measure.check_and_get(
            {'conflicts': 1234}, True), (1234, Status.RESOLVED)
        )

    def test_propagation(self):
        measure = Propagations()
        self.assertEqual(measure.get_budget(), ('propagations', None))
        self.assertEqual(measure.check_and_get(
            {'propagations': 1234}, False), (1234, Status.SOLVED)
        )

    def test_learned_literals(self):
        measure = LearnedLiterals()
        self.assertEqual(measure.get_budget(), ('learned_literals', None))
        self.assertEqual(measure.check_and_get(
            {'learned_literals': 1234}, None), (1234, Status.INTERRUPTED)
        )
