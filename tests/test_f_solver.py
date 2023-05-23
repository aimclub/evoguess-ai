import unittest

from function.model import Status
from function.module.budget import TaskBudget
from instance.module.encoding import CNF

from function.module.solver import pysat, TwoSAT
from function.module.measure import Propagations, SolvingTime


class TestSolver(unittest.TestCase):
    def test_pysat(self):
        solver = pysat.Glucose3()
        measure = Propagations()
        budget = TaskBudget(None)
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        encoding_data = CNF(from_clauses=clauses).get_data()

        report = solver.propagate(encoding_data, ([], []))
        self.assertEqual(
            (report.status, report.model),
            (False, [])
        )
        _, value, status = measure.check_and_get(report, budget)
        self.assertEqual((value, status), (0, Status.SOLVED))

        report = solver.propagate(encoding_data, ([-1], []))
        self.assertEqual((report.status, report.model), (False, [-1, 2]))
        _, value, status = measure.check_and_get(report, budget)
        self.assertEqual((value, status), (2, Status.SOLVED))

        report = solver.solve(encoding_data, ([], []), add_model=True)
        self.assertEqual((report.status, report.model), (True, [-1, 2, -3, -4]))
        _, value, status = measure.check_and_get(report, budget)
        self.assertEqual((value, status), (5, Status.RESOLVED))

        report = solver.solve(encoding_data, ([1], []), add_model=True)
        self.assertEqual((report.status, report.model), (True, [1, 2, -3, -4]))
        _, value, status = measure.check_and_get(report, budget)
        self.assertEqual((value, status), (5, Status.RESOLVED))

        with solver.use_incremental(encoding_data) as incremental:
            report = incremental.propagate([])
            _, value, status = measure.check_and_get(report, budget)
            self.assertEqual((value, status, report.model), (0, Status.SOLVED, []))

            report = incremental.propagate([-1])
            _, value, status = measure.check_and_get(report, budget)
            self.assertEqual((value, status, report.model), (2, Status.SOLVED, [-1, 2]))

            report = incremental.propagate([1])
            _, value, status = measure.check_and_get(report, budget)
            self.assertEqual((value, status, report.model), (1, Status.SOLVED, [1]))

        limit = measure.get_limit(TaskBudget(6))
        report = solver.solve(encoding_data, ([], []), limit)
        _, value, status = measure.check_and_get(report, budget)
        self.assertEqual((value, status, report.model), (5, Status.RESOLVED, None))

        measure = Propagations(at_least=8)
        report = solver.solve(encoding_data, ([], []))
        _, value, status = measure.check_and_get(report, budget)
        self.assertEqual((value, status, report.model), (5, Status.NOT_REACHED, None))

    # def test_pysat_by_time(self):
    #     with solver.use_incremental(data, SolvingTime()) as incremental:
    #         status, stats, model = incremental.solve([])
    #         self.assertEqual((status, model), (Status.RESOLVED, [-1, 2, -3, -4]))
    #         status, stats, model = incremental.solve([1])
    #         self.assertEqual((status, model), (Status.RESOLVED, [1, 2, -3, -4]))

    def test_two_sat(self):
        solver = TwoSAT()
        measure = Propagations()
        budget = TaskBudget(None)
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        encoding_data = CNF(from_clauses=clauses).get_data()

        report = solver.propagate(encoding_data, ([], []))
        _, value, status = measure.check_and_get(report, budget)
        self.assertEqual((value, status, report.model), (0, Status.INTERRUPTED, []))

        with solver.use_incremental(encoding_data) as incremental:
            status, _, model = incremental.solve([2])
            self.assertEqual((status, model), (False, [2]))
            status, _, model = incremental.propagate([-1, 2, -3, -4])
            self.assertEqual((status, model), (True, [-1, 2, -3, -4]))
