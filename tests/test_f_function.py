import unittest

from function.models import ChunkResult
from function.impl import GuessAndDetermine, \
    InverseBackdoorSets, InversePolynomialSets, RhoFunction

from function.impl.function_gad import gad_worker_fn
from function.impl.function_ibs import ibs_worker_fn
from function.impl.function_ips import ips_worker_fn
from function.impl.function_rho import rho_worker_fn

from function.module.solver import pysat, TwoSAT
from function.module.measure import Propagations

from instance.impl import Instance, StreamCipher
from core.module.space import SearchSet, InputSet

from instance.module.encoding import CNF
from instance.module.variables import Interval, Indexes


class TestFunction(unittest.TestCase):
    def test_gad_function(self):
        solver = pysat.Glucose3()
        measure = Propagations()
        function = GuessAndDetermine(solver, measure)

        space = SearchSet(Interval(start=1, length=4))
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

    def test_ibs_function(self):
        solver = pysat.Glucose3()
        measure = Propagations(budget=10)
        function = InverseBackdoorSets(solver, measure)

        space = InputSet()
        clauses = [[-1, -2], [1, 3], [2, -4], [-3, 4]]
        instance = StreamCipher(
            encoding=CNF(from_clauses=clauses),
            input_set=Indexes(from_iterable=[1, 2]),
            output_set=Indexes(from_iterable=[3, 4])
        )

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

        space = InputSet()
        clauses = [[-1, -2], [1, 3], [2, -4], [-3, 4]]
        instance = StreamCipher(
            encoding=CNF(from_clauses=clauses),
            input_set=Indexes(from_iterable=[1, 2]),
            output_set=Indexes(from_iterable=[3, 4])
        )

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
        self.assertEqual(estimation['statuses'], {0: 2, 1: 2})

    def test_rho_function(self):
        solver = pysat.Glucose3()
        measure = Propagations()
        function = RhoFunction(solver, measure, 2 ** 10)

        space = SearchSet(Interval(start=1, length=4))
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
