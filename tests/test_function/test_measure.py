import unittest

from function.model import Status
from pysatmc.solver import Report

from function.module.budget import TaskBudget
from function.module.measure import SolvingTime, \
    Propagations, Conflicts, LearnedLiterals


class TestMeasure(unittest.TestCase):
    def test_solving_time(self):
        budget = TaskBudget(None)
        measure = SolvingTime()
        self.assertEqual(measure.get_limit(budget), ('', None))

        report = Report(True, {'time': 56}, None)
        self.assertEqual(
            measure.check_and_get(report, budget),
            (56, 56, Status.RESOLVED)
        )

        report = Report(None, {'time': 3.2}, None)
        self.assertEqual(
            measure.check_and_get(report, budget),
            (3.2, 3.2, Status.INTERRUPTED)
        )

        budget = TaskBudget(value=6.5)
        measure = SolvingTime(at_least=3.2)
        self.assertEqual(measure.get_limit(budget), ('time', 6.5))

        report = Report(None, {'time': 6.6}, None)
        self.assertEqual(
            measure.check_and_get(report, budget),
            (6.6, 6.6, Status.EXHAUSTED)
        )

        report = Report(True, {'time': 3.1}, None)
        self.assertEqual(
            measure.check_and_get(report, budget),
            (3.1, 3.1, Status.NOT_REACHED)
        )

    def test_conflicts(self):
        measure = Conflicts()
        budget = TaskBudget(10000)
        self.assertEqual(measure.get_limit(budget), ('conflicts', 10000))

        report = Report(True, {'conflicts': 1234}, None)
        self.assertEqual(
            measure.check_and_get(report, budget), (None, 1234, Status.RESOLVED)
        )

    def test_propagation(self):
        measure = Propagations()
        budget = TaskBudget(None)
        self.assertEqual(measure.get_limit(budget), ('', None))

        report = Report(True, {'propagations': 1234}, None)
        self.assertEqual(
            measure.check_and_get(report, budget), (None, 1234, Status.RESOLVED)
        )

    def test_learned_literals(self):
        measure = LearnedLiterals()
        budget = TaskBudget(None)
        self.assertEqual(measure.get_limit(budget), ('', None))

        report = Report(None, {'learned_literals': 1234}, None)
        self.assertEqual(
            measure.check_and_get(report, budget),
            (None, 1234, Status.INTERRUPTED)
        )
