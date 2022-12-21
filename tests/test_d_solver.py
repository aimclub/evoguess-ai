import unittest

from function.models import Status
from instance.module.encoding import CNF

from function.module.solver import pysat, TwoSAT
from function.module.measure import Propagations, SolvingTime


class TestSolver(unittest.TestCase):
    def test_pysat(self):
        solver = pysat.Glucose3()
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        data = CNF(from_clauses=clauses).get_data()

        _, value, status, model = solver.propagate(data, Propagations(), ([], []))
        self.assertEqual((value, status, model), (0, Status.SOLVED, []))
        _, value, status, model = solver.propagate(data, Propagations(), ([-1], []))
        self.assertEqual((value, status, model), (2, Status.SOLVED, [-1, 2]))

        _, value, status, model = solver.solve(data, Propagations(), ([], []))
        self.assertEqual((value, status, model), (5, Status.RESOLVED, [-1, 2, -3, -4]))
        _, value, status, model = solver.solve(data, Propagations(), ([1], []))
        self.assertEqual((value, status, model), (5, Status.RESOLVED, [1, 2, -3, -4]))

        with solver.use_incremental(data, Propagations()) as incremental:
            _, value, status, model = incremental.propagate([])
            self.assertEqual((value, status, model), (0, Status.SOLVED, []))
            _, value, status, model = incremental.propagate([-1])
            self.assertEqual((value, status, model), (2, Status.SOLVED, [-1, 2]))
            _, value, status, model = incremental.propagate([1], add_model=False)
            self.assertEqual((value, status, model), (1, Status.SOLVED, None))

        with solver.use_incremental(data, SolvingTime()) as incremental:
            _, _, status, model = incremental.solve([])
            self.assertEqual((status, model), (Status.RESOLVED, [-1, 2, -3, -4]))
            _, _, status, model = incremental.solve([1])
            self.assertEqual((status, model), (Status.RESOLVED, [1, 2, -3, -4]))
            _, _, status, model = incremental.solve([1], add_model=False)
            self.assertEqual((status, model), (Status.RESOLVED, None))

        _, value, status, model = solver.solve(data, Propagations(budget=3), ([], []))
        self.assertEqual((value, status, model), (5, Status.RESOLVED, [-1, 2, -3, -4]))
        _, value, status, model = solver.solve(data, Propagations(at_least=8), ([], []))
        self.assertEqual((value, status, model), (5, Status.NOT_REACHED, [-1, 2, -3, -4]))

    def test_two_sat(self):
        solver = TwoSAT()
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        data = CNF(from_clauses=clauses).get_data()

        _, value, status, model = solver.propagate(data, Propagations(), ([], []))
        self.assertEqual((value, status, model), (0, Status.EXHAUSTED, []))

        with solver.use_incremental(data, Propagations()) as incremental:
            _, _, status, model = incremental.solve([2])
            self.assertEqual((status, model), (Status.SOLVED, [2]))
            _, _, status, model = incremental.propagate([-1, 2, -3, -4])
            self.assertEqual((status, model), (Status.RESOLVED, [-1, 2, -3, -4]))
            _, _, status, model = incremental.propagate([2], add_model=False)
            self.assertEqual((status, model), (Status.SOLVED, None))
