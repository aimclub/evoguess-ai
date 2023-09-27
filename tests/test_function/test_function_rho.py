import unittest

from pysatmc.encoding import CNF
from pysatmc.variables import Range
from pysatmc.problem import SatProblem
from pysatmc.solver import PySatSolver

from function.impl import RhoFunction
from function.model import ChunkResult
from function.module.measure import Propagations
from function.impl.function_rho import rho_worker_fn

from space.impl import BackdoorSet


class TestFunction(unittest.TestCase):
    def test_rho_function(self):
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        problem = SatProblem(
            solver=PySatSolver(), encoding=CNF(from_clauses=clauses)
        )
        space = BackdoorSet(variables=Range(start=1, length=4))
        function = RhoFunction(Propagations(), 2 ** 10)

        backdoor = space.get_initial()
        payload = function.get_payload(space, problem, backdoor)
        budget, measure = function.budget, function.measure
        self.assertEqual(
            payload, (space, budget, measure, problem, backdoor.pack())
        )

        worker_fn = function.get_worker_fn()
        self.assertEqual(worker_fn, rho_worker_fn)

        estimation = function.calculate(backdoor, [
            ChunkResult(*worker_fn((43, 16, 0, 16), payload))
        ])
        self.assertEqual(estimation['count'], 16)
        self.assertEqual(estimation['value'], 394.0)
        self.assertEqual(
            estimation['statuses'], {'RESOLVED': 10, 'SOLVED': 6}
        )
