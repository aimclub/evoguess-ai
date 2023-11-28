import unittest

from lib_satprob.solver import PySatSolver
from lib_satprob.encoding import CNF, WCNF


class TestSolver(unittest.TestCase):
    def test_pysat_sat(self):
        solver = PySatSolver()
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        formula = CNF(from_clauses=clauses).get_formula()

        status, stats, model, _ = solver.propagate(formula, ([], []))
        self.assertEqual(
            (status, stats['propagations'], model), (None, 0, [])
        )

        status, stats, model, _ = solver.propagate(formula, ([-1], []))
        self.assertEqual(
            (status, stats['propagations'], model), (None, 2, [-1, 2])
        )

        _, stats, model, _ = solver.solve(formula, ([], []),
                                          extract_model=False)
        self.assertEqual((stats['propagations'], model), (5, None))

        status, stats, model, _ = solver.solve(formula, ([], []))
        self.assertEqual(
            (status, stats['propagations'], model), (True, 5, [-1, 2, -3, -4])
        )

        status, stats, model, _ = solver.solve(formula, ([1], []))
        self.assertEqual(
            (status, stats['propagations'], model), (True, 5, [1, 2, -3, -4])
        )

        with solver.get_instance(formula) as incremental:
            status, stats, model, _ = incremental.propagate(([], []))
            self.assertEqual(
                (status, stats['propagations'], model), (None, 0, [])
            )

            status, stats, model, _ = incremental.propagate(([-1], []))
            self.assertEqual(
                (status, stats['propagations'], model), (None, 2, [-1, 2])
            )

            status, stats, model, _ = incremental.propagate(([1], []))
            self.assertEqual(
                (status, stats['propagations'], model), (None, 3, [1])
            )

        limit = ('propagations', 6)
        status, stats, model, _ = solver.solve(formula, ([], []), limit)
        self.assertEqual(
            (status, stats['propagations'], model), (True, 5, [-1, 2, -3, -4])
        )

    def test_pysat_max_sat(self):
        # todo: add MaxSat tests
        pass

    def test_pysat_family(self):
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        formula = CNF(from_clauses=clauses).get_formula()

        # report = PySatSolver(sat_name='cd').solve(formula, ([], []))
        # self.assertEqual((report.status, report.model), (True, []))

        report = PySatSolver(sat_name='g3').solve(formula, ([], []))
        self.assertEqual((report.status, report.model), (True, [-1, 2, -3, -4]))

        report = PySatSolver(sat_name='g4').solve(formula, ([], []))
        self.assertEqual((report.status, report.model), (True, [-1, 2, -3, -4]))

    # todo: TwoSat solver restore
    # def test_pysat_by_time(self):
    #     with solver.use_incremental(data, SolvingTime()) as incremental:
    #         status, stats, model = incremental.solve([])
    #         self.assertEqual((status, model), (True, [-1, 2, -3, -4]))
    #         status, stats, model = incremental.solve([1])
    #         self.assertEqual((status, model), (True, [1, 2, -3, -4]))

    # def test_two_sat(self):
    #     solver = TwoSAT()
    #     measure = Propagations()
    #     budget = TaskBudget(None)
    #     clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
    #     encoding_data = CNF(from_clauses=clauses).get_data()
    #
    #     report = solver.propagate(encoding_data, ([], []))
    #     _, value, status = measure.check_and_get(report, budget)
    #     self.assertEqual((value, status, report.model), (0, None, []))
    #
    #     with solver.get_instance(encoding_data) as incremental:
    #         status, _, model = incremental.solve([2])
    #         self.assertEqual((status, model), (False, [2]))
    #         status, _, model = incremental.propagate([-1, 2, -3, -4])
    #         self.assertEqual((status, model), (True, [-1, 2, -3, -4]))
