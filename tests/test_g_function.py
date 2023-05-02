import unittest

from function.model import ChunkResult
from function.impl import GuessAndDetermine, \
    InverseBackdoorSets, InversePolynomialSets, RhoFunction

from function.impl.function_gad import gad_worker_fn, gad_supplements
from function.impl.function_ibs import ibs_worker_fn, ibs_supplements
from function.impl.function_ips import ips_worker_fn
from function.impl.function_rho import rho_worker_fn

from function.module.solver import pysat, TwoSAT
from function.module.measure import Propagations

from space.impl import BackdoorSet, IntervalSet
from instance.impl import Instance, StreamCipher

from instance.module.encoding import CNF
from instance.module.variables import Range, Indexes


class TestFunction(unittest.TestCase):
    def test_gad_backdoor_supplements(self):
        variables = Indexes(from_iterable=[1, 2])
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        instance = Instance(encoding=CNF(from_clauses=clauses))
        backdoor = BackdoorSet(variables=variables).get_initial(instance)

        for supplements, test_supplements in zip(
                gad_supplements((43, 8, 0, 8), instance, backdoor),
                [([1, -2], []), ([-1, 2], []), ([1, 2], []), ([-1, -2], []),
                 ([1, -2], []), ([-1, -2], []), ([1, 2], []), ([-1, 2], [])]
        ): self.assertTupleEqual(supplements, test_supplements)
        for supplements, test_supplements in zip(
                gad_supplements((43, 8, 0, 4), instance, backdoor),
                [([1, -2], []), ([-1, 2], []), ([1, 2], []), ([-1, -2], [])]
        ):  self.assertTupleEqual(supplements, test_supplements)
        for supplements, test_supplements in zip(
                gad_supplements((43, 8, 4, 4), instance, backdoor),
                [([1, -2], []), ([-1, -2], []), ([1, 2], []), ([-1, 2], [])]
        ):  self.assertTupleEqual(supplements, test_supplements)

        variables = Indexes(from_iterable=[1, 3, 4])
        backdoor = BackdoorSet(variables=variables).get_initial(instance)
        for supplements, test_supplements in zip(
                gad_supplements((21, 8, 2, 6), instance, backdoor),
                [([-1, 3, 4], []), ([1, -3, 4], []), ([1, 3, -4], []),
                 ([1, -3, -4], []), ([-1, -3, -4], []), ([-1, -3, 4], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        backdoor = backdoor.make_copy([])
        for supplements, test_supplements in zip(
                gad_supplements((93, 90, 6, 56), instance, backdoor),
                [([], []), ([], []), ([], []), ([], []), ([], []), ([], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

    def test_gad_interval_supplements(self):
        indexes = Indexes(from_iterable=[1, 2, 3])
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        instance = Instance(encoding=CNF(from_clauses=clauses))
        interval = IntervalSet(indexes=indexes).get_initial(instance)

        for supplements, test_supplements in zip(
                gad_supplements((43, 8, 2, 6), instance, interval),
                [([1, -2, 3], []), ([1, 2, -3], []), ([-1, 2, -3], []),
                 ([-1, -2, 3], []), ([-1, -2, -3], []), ([1, -2, -3], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        interval = interval.make_copy([0, 1, 0])
        for supplements, test_supplements in zip(
                gad_supplements((43, 4, 1, 3), instance, interval),
                [([-1], [[-2, -3]]), ([-1], [[-2, -3]]), ([-1], [[-2, -3]])]
        ): self.assertTupleEqual(supplements, test_supplements)

        interval = interval.make_copy([0, 0, 0])
        for supplements, test_supplements in zip(
                gad_supplements((123, 90, 6, 56), instance, interval),
                [([], []), ([], []), ([], []), ([], []), ([], []), ([], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

    def test_gad_function(self):
        solver = pysat.Glucose3()
        measure = Propagations()
        function = GuessAndDetermine(solver, measure)

        space = BackdoorSet(Range(start=1, length=4))
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        instance = Instance(encoding=CNF(from_clauses=clauses))

        backdoor = space.get_initial(instance)
        payload = function.get_payload(space, instance, backdoor)
        self.assertEqual(payload, (space, solver, measure, instance, backdoor.pack()))

        worker_fn = function.get_worker_fn()
        self.assertEqual(worker_fn, gad_worker_fn)

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 16, 0, 16), payload))
        ])
        self.assertEqual(estimation['count'], 16)
        self.assertEqual(estimation['value'], 64.0)
        self.assertEqual(estimation['statuses'], {1: 10, 0: 6})

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 16, 0, 8), payload)),
            ChunkResult(*worker_fn((43, 16, 8, 8), payload))
        ])
        self.assertEqual(estimation['count'], 16)
        self.assertEqual(estimation['value'], 64.0)
        self.assertEqual(estimation['statuses'], {1: 10, 0: 6})

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 16, 0, 4), payload)),
            ChunkResult(*worker_fn((43, 16, 4, 4), payload)),
            ChunkResult(*worker_fn((43, 16, 8, 4), payload)),
            ChunkResult(*worker_fn((43, 16, 12, 4), payload))
        ])
        self.assertEqual(estimation['count'], 16)
        self.assertEqual(estimation['value'], 64.0)
        self.assertEqual(estimation['statuses'], {1: 10, 0: 6})

        estimation = function.calculate(backdoor, [])
        self.assertEqual(estimation['count'], 0)
        self.assertEqual(estimation['value'], float('inf'))

    def test_ibs_backdoor_supplements(self):
        instance = StreamCipher(
            encoding=CNF(from_clauses=[
                [-1, 3], [1, -3], [2, -4], [-2, -4],
            ]),
            input_set=Indexes(from_iterable=[1, 2]),
            output_set=Indexes(from_iterable=[3, 4])
        )

        variables = instance.input_set
        backdoor = BackdoorSet(variables=variables).get_initial(instance)
        for supplements, test_supplements in zip(
                ibs_supplements((41, 8, 2, 6), instance, backdoor),
                [([-1, 2, -3, -4], []), ([1, 2, 3, -4], []), ([1, 2, 3, -4], []),
                 ([-1, 2, -3, -4], []), ([-1, -2, -3, -4], []), ([1, 2, 3, -4], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        backdoor = backdoor.make_copy([1])
        for supplements, test_supplements in zip(
                ibs_supplements((23, 7, 4, 3), instance, backdoor),
                [([-1, -3, -4], []), ([1, 3, -4], []), ([1, 3, -4], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        backdoor = backdoor.make_copy([])
        for supplements, test_supplements in zip(
                ibs_supplements((11, 8, 4, 4), instance, backdoor),
                [([3, -4], []), ([-3, -4], []), ([3, -4], []), ([-3, -4], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

    def test_ibs_interval_supplements(self):
        instance = StreamCipher(
            encoding=CNF(from_clauses=[
                [-1, 4], [1, -4], [2, -5],
                [-2, -5], [-3, -6], [3, 6],
            ]),
            input_set=Indexes(from_iterable=[1, 2, 3]),
            output_set=Indexes(from_iterable=[4, 5, 6])
        )

        indexes = instance.input_set
        interval = IntervalSet(indexes=indexes).get_initial(instance)
        for supplements, test_supplements in zip(
                ibs_supplements((41, 6, 2, 4), instance, interval),
                [([1, 2, 3, 4, -5, -6], []), ([1, -2, 3, 4, -5, -6], []),
                 ([-1, -2, 3, -4, -5, -6], []), ([1, -2, -3, 4, -5, 6], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

        interval = interval.make_copy([0, 1, 0])
        for supplements, test_supplements in zip(
                ibs_supplements((15, 32, 24, 4), instance, interval),
                [([4, -5, 6], [[1, 2], [1, 3], [-1, -2]]), ([1, 2, 4, -5, -6], []),
                 ([-1, -4, -5, 6], [[-2, -3]]), ([-1, -4, -5, -6], [[-2, -3]])]
        ): self.assertTupleEqual(supplements, test_supplements)

        interval = interval.make_copy([0, 0, 0])
        for supplements, test_supplements in zip(
                ibs_supplements((15, 32, 24, 3), instance, interval),
                [([4, -5, 6], []), ([4, -5, -6], []), ([-4, -5, 6], [])]
        ): self.assertTupleEqual(supplements, test_supplements)

    def test_ibs_function(self):
        solver = pysat.Glucose3()
        measure = Propagations(budget=10)
        function = InverseBackdoorSets(solver, measure)

        clauses = [[-1, -2], [1, 3], [2, -4], [-3, 4]]
        instance = StreamCipher(
            encoding=CNF(from_clauses=clauses),
            input_set=Indexes(from_iterable=[1, 2]),
            output_set=Indexes(from_iterable=[3, 4])
        )
        space = BackdoorSet(instance.input_set)

        backdoor = space.get_initial(instance)
        payload = function.get_payload(space, instance, backdoor)
        self.assertEqual(payload, (space, solver, measure, instance, backdoor.pack()))

        worker_fn = function.get_worker_fn()
        self.assertEqual(worker_fn, ibs_worker_fn)

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 4, 0, 4), payload))
        ])
        self.assertEqual(estimation['count'], 4)
        self.assertEqual(estimation['value'], 120.0)
        self.assertEqual(estimation['statuses'], {1: 4})

    def test_ips_function(self):
        solver = TwoSAT()
        measure = Propagations(budget=10)
        function = InversePolynomialSets(solver, measure)

        clauses = [[-1, -2], [1, 3], [2, -4], [-3, 4]]
        instance = StreamCipher(
            encoding=CNF(from_clauses=clauses),
            input_set=Indexes(from_iterable=[1, 2]),
            output_set=Indexes(from_iterable=[3, 4])
        )
        space = BackdoorSet(instance.input_set)

        backdoor = space.get_initial(instance)
        payload = function.get_payload(space, instance, backdoor)
        self.assertEqual(payload, (space, solver, measure, instance, backdoor.pack()))

        worker_fn = function.get_worker_fn()
        self.assertEqual(worker_fn, ips_worker_fn)

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 4, 0, 4), payload))
        ])
        self.assertEqual(estimation['count'], 4)
        self.assertEqual(estimation['value'], 12.0)
        self.assertEqual(estimation['statuses'], {1: 4})

    def test_rho_function(self):
        solver = pysat.Glucose3()
        measure = Propagations()
        function = RhoFunction(solver, measure, 2 ** 10)

        space = BackdoorSet(Range(start=1, length=4))
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        instance = Instance(encoding=CNF(from_clauses=clauses))

        backdoor = space.get_initial(instance)
        payload = function.get_payload(space, instance, backdoor)
        self.assertEqual(payload, (space, solver, measure, instance, backdoor.pack()))

        worker_fn = function.get_worker_fn()
        self.assertEqual(worker_fn, rho_worker_fn)

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 16, 0, 16), payload))
        ])
        self.assertEqual(estimation['count'], 16)
        self.assertEqual(estimation['value'], 16.0)
        self.assertEqual(estimation['statuses'], {1: 16})
