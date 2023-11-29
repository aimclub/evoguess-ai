import unittest

from lib_satprob.encoding import CNF
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem
from lib_satprob.variables import Indexes, Range

from function.model import ChunkResult
from function.impl import GuessAndDetermine
from function.module.budget import AutoBudget
from function.module.measure import Propagations
from function.impl.function_gad import gad_worker_fn, gad_supplements

from space.impl import BackdoorSet, IntervalSet


class TestFunction(unittest.TestCase):
    def test_gad_backdoor_supplements(self):
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        space = BackdoorSet(variables=Indexes(from_iterable=[1, 2]))
        problem = SatProblem(
            solver=PySatSolver(), encoding=CNF(from_clauses=clauses)
        )

        backdoor = space.get_initial()
        for supplements, test_supplements in zip(
                gad_supplements((43, 8, 0, 8), problem, backdoor),
                [([1, -2], []), ([-1, 2], []), ([1, 2], []), ([-1, -2], []),
                 ([1, -2], []), ([-1, -2], []), ([1, 2], []), ([-1, 2], [])]
        ): self.assertTupleEqual(supplements, test_supplements)
        for supplements, test_supplements in zip(
                gad_supplements((43, 8, 0, 4), problem, backdoor),
                [([1, -2], []), ([-1, 2], []), ([1, 2], []), ([-1, -2], [])]
        ):  self.assertTupleEqual(supplements, test_supplements)
        for supplements, test_supplements in zip(
                gad_supplements((43, 8, 4, 4), problem, backdoor),
                [([1, -2], []), ([-1, -2], []), ([1, 2], []), ([-1, 2], [])]
        ):  self.assertTupleEqual(supplements, test_supplements)

        space = BackdoorSet(variables=Indexes(from_iterable=[1, 3, 4]))
        backdoor = space.get_initial()
        for supplements, test_supplements in zip(
                gad_supplements((21, 8, 2, 6), problem, backdoor),
                [([-1, 3, 4], []), ([1, -3, 4], []), ([1, 3, -4], []),
                 ([1, -3, -4], []), ([-1, -3, -4], []), ([-1, -3, 4], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        backdoor = backdoor.make_copy([])
        for supplements, test_supplements in zip(
                gad_supplements((93, 90, 6, 56), problem, backdoor),
                [([], []), ([], []), ([], []), ([], []), ([], []), ([], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

    def test_gad_interval_supplements(self):
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        space = IntervalSet(indexes=Indexes(from_iterable=[1, 2, 3]))
        problem = SatProblem(
            solver=PySatSolver(), encoding=CNF(from_clauses=clauses)
        )

        interval = space.get_initial()
        for supplements, test_supplements in zip(
                gad_supplements((43, 8, 2, 6), problem, interval),
                [([1, -2, 3], []), ([1, 2, -3], []), ([-1, 2, -3], []),
                 ([-1, -2, 3], []), ([-1, -2, -3], []), ([1, -2, -3], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        interval = interval.make_copy([0, 1, 0])
        for supplements, test_supplements in zip(
                gad_supplements((43, 4, 1, 3), problem, interval),
                [([-1], [[-2, -3]]), ([-1], [[-2, -3]]), ([-1], [[-2, -3]])]
        ): self.assertTupleEqual(supplements, test_supplements)

        interval = interval.make_copy([0, 0, 0])
        for supplements, test_supplements in zip(
                gad_supplements((123, 90, 6, 56), problem, interval),
                [([], []), ([], []), ([], []), ([], []), ([], []), ([], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

    def test_gad_function(self):
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        space = BackdoorSet(variables=Range(start=1, length=4))
        problem = SatProblem(
            solver=PySatSolver(), encoding=CNF(from_clauses=clauses)
        )

        backdoor = space.get_initial()
        budget, measure = AutoBudget(), Propagations()
        function = GuessAndDetermine(budget, measure)
        payload = function.get_payload(space, problem, backdoor)
        self.assertEqual(
            payload, (space, budget, measure, problem, backdoor.pack())
        )

        worker_fn = function.get_worker_fn()
        self.assertEqual(worker_fn, gad_worker_fn)

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 16, 0, 16), payload))
        ])
        self.assertEqual(estimation['count'], 16)
        self.assertEqual(estimation['value'], 64.0)
        self.assertEqual(
            estimation['statuses'], {'RESOLVED': 10, 'SOLVED': 6}
        )

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 16, 0, 8), payload)),
            ChunkResult(*worker_fn((43, 16, 8, 8), payload))
        ])
        self.assertEqual(estimation['count'], 16)
        self.assertEqual(estimation['value'], 64.0)
        self.assertEqual(
            estimation['statuses'], {'RESOLVED': 10, 'SOLVED': 6}
        )

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 16, 0, 4), payload)),
            ChunkResult(*worker_fn((43, 16, 4, 4), payload)),
            ChunkResult(*worker_fn((43, 16, 8, 4), payload)),
            ChunkResult(*worker_fn((43, 16, 12, 4), payload))
        ])
        self.assertEqual(estimation['count'], 16)
        self.assertEqual(estimation['value'], 64.0)
        self.assertEqual(
            estimation['statuses'], {'RESOLVED': 10, 'SOLVED': 6}
        )

        estimation = function.calculate(backdoor, [])
        self.assertEqual(estimation['count'], 0)
        self.assertEqual(estimation['value'], float('inf'))
