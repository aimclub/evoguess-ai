import unittest

from pysatmc.encoding import CNF
from pysatmc.variables import Indexes
from pysatmc.problem import SatProblem
from pysatmc.solver import PySatSolver

from function.model import ChunkResult
from function.impl import InverseBackdoorSets
from function.module.budget import TaskBudget
from function.module.measure import Propagations
from function.impl.function_ibs import ibs_worker_fn, ibs_supplements

from space.impl import BackdoorSet, IntervalSet


class TestFunctionIBS(unittest.TestCase):
    def test_ibs_backdoor_supplements(self):
        clauses = [[-1, 3], [1, -3], [2, -4], [-2, -4]]
        problem = SatProblem(
            input_set=Indexes(from_iterable=[1, 2]),
            output_set=Indexes(from_iterable=[3, 4]),
            solver=PySatSolver(), encoding=CNF(from_clauses=clauses)
        )
        space = BackdoorSet(variables=problem.input_set)

        backdoor = space.get_initial()
        for supplements, test_supplements in zip(
                ibs_supplements((41, 8, 2, 6), problem, backdoor),
                [([-1, 2, -3, -4], []), ([1, 2, 3, -4], []),
                 ([1, 2, 3, -4], []), ([-1, 2, -3, -4], []),
                 ([-1, -2, -3, -4], []), ([1, 2, 3, -4], [])]
        ): self.assertTupleEqual(supplements, test_supplements)
        #
        for supplements, test_supplements in zip(
                ibs_supplements((41, 8, 2, 6), problem, backdoor),
                [([-1, 2, -3, -4], []), ([1, 2, 3, -4], []),
                 ([1, 2, 3, -4], []), ([-1, 2, -3, -4], []),
                 ([-1, -2, -3, -4], []), ([1, 2, 3, -4], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        backdoor = backdoor.make_copy([1])
        for supplements, test_supplements in zip(
                ibs_supplements((23, 7, 4, 3), problem, backdoor),
                [([-1, -3, -4], []), ([1, 3, -4], []), ([1, 3, -4], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        backdoor = backdoor.make_copy([])
        for supplements, test_supplements in zip(
                ibs_supplements((11, 8, 4, 4), problem, backdoor),
                [([3, -4], []), ([-3, -4], []), ([3, -4], []), ([-3, -4], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

    def test_ibs_interval_supplements(self):
        clauses = [[-1, 4], [1, -4], [2, -5], [-2, -5], [-3, -6], [3, 6]]
        problem = SatProblem(
            input_set=Indexes(from_iterable=[1, 2, 3]),
            output_set=Indexes(from_iterable=[4, 5, 6]),
            solver=PySatSolver(), encoding=CNF(from_clauses=clauses)
        )
        space = IntervalSet(indexes=problem.input_set)

        interval = space.get_initial()
        for supplements, test_supplements in zip(
                ibs_supplements((41, 6, 2, 4), problem, interval),
                [([1, 2, 3, 4, -5, -6], []), ([1, -2, 3, 4, -5, -6], []),
                 ([-1, -2, 3, -4, -5, -6], []), ([1, -2, -3, 4, -5, 6], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        interval = interval.make_copy([0, 1, 0])
        for supplements, test_supplements in zip(
                ibs_supplements((15, 32, 24, 4), problem, interval),
                [([4, -5, 6], [[1, 2], [1, 3], [-1, -2]]),
                 ([1, 2, 4, -5, -6], []), ([-1, -4, -5, 6], [[-2, -3]]),
                 ([-1, -4, -5, -6], [[-2, -3]])]
        ): self.assertTupleEqual(supplements, test_supplements)

        interval = interval.make_copy([0, 0, 0])
        for supplements, test_supplements in zip(
                ibs_supplements((15, 32, 24, 3), problem, interval),
                [([4, -5, 6], []), ([4, -5, -6], []), ([-4, -5, 6], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

    def test_ibs_function(self):
        clauses = [[-1, -2], [1, 3], [2, -4], [-3, 4]]
        problem = SatProblem(
            input_set=Indexes(from_iterable=[1, 2]),
            output_set=Indexes(from_iterable=[3, 4]),
            solver=PySatSolver(), encoding=CNF(from_clauses=clauses)
        )
        space = BackdoorSet(variables=problem.input_set)

        backdoor = space.get_initial()
        budget, measure = TaskBudget(10), Propagations()
        function = InverseBackdoorSets(budget, measure)
        payload = function.get_payload(space, problem, backdoor)
        self.assertEqual(
            payload, (space, budget, measure, problem, backdoor.pack())
        )

        worker_fn = function.get_worker_fn()
        self.assertEqual(worker_fn, ibs_worker_fn)

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 4, 0, 4), payload))
        ])
        self.assertEqual(estimation['count'], 4)
        self.assertEqual(estimation['value'], 120.0)
        self.assertEqual(estimation['statuses'], {'RESOLVED': 4})
