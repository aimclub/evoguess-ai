import unittest

from pysatmc.encoding import CNF
from pysatmc.variables import Indexes
from pysatmc.problem import SatProblem

from function.model import ChunkResult
from function.impl import InversePolynomialSets
from function.impl.function_ips import ips_worker_fn
#
from function.module.measure import Propagations
from function.module.budget import AutoBudget, TaskBudget

from space.impl import BackdoorSet, IntervalSet


class TestFunction(unittest.TestCase):
    def test_ips_function(self):
        # todo: make 2SAT solver
        clauses = [[-1, -2], [1, 3], [2, -4], [-3, 4]]
        problem = SatProblem(
            input_set=Indexes(from_iterable=[1, 2]),
            output_set=Indexes(from_iterable=[3, 4]),
            solver=None, encoding=CNF(from_clauses=clauses)
        )
        space = BackdoorSet(variables=problem.input_set)
        function = InversePolynomialSets(Propagations())

        backdoor = space.get_initial()
        payload = function.get_payload(space, problem, backdoor)
        budget, measure = function.budget, function.measure
        self.assertEqual(
            payload, (space, budget, measure, problem, backdoor.pack())
        )

        worker_fn = function.get_worker_fn()
        self.assertEqual(worker_fn, ips_worker_fn)
#
#         estimation = function.calculate(backdoor, [
#             ChunkResult(*worker_fn((43, 4, 0, 4), payload))
#         ])
#         self.assertEqual(estimation['count'], 4)
#         self.assertEqual(estimation['value'], 12.0)
#         self.assertEqual(
#             estimation['statuses'],
#             {'RESOLVED': 4}
#         )
#
