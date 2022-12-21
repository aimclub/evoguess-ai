from os import getpid
from time import time as now

from ..abc.function import aggregate_results
from ..models import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation, Status
from .function_ibs import InverseBackdoorSets, ibs_supplements

from function.module.solver import Solver
from function.module.measure import Measure
from instance.module.variables import Backdoor


def ips_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    backdoor, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    encoding_data = instance.encoding.get_data()
    with solver.use_incremental(encoding_data, measure) as incremental:
        for assumptions, _ in ibs_supplements(args, instance, backdoor):
            # todo: use constraints with incremental propagation?
            time, value, status, _ = incremental.propagate(assumptions, add_model=False)

            times[status.value] = times.get(status.value, 0.) + time
            values[status.value] = values.get(status.value, 0.) + value
            statuses[status.value] = statuses.get(status.value, 0) + 1
    return getpid(), now() - timestamp, times, values, statuses, args


class InversePolynomialSets(InverseBackdoorSets):
    slug = 'function:ips'

    def __init__(self, solver: Solver, measure: Measure, min_solved: float = 0.):
        super().__init__(solver, measure)
        self.min_solved = min_solved

    def get_worker_fn(self) -> WorkerCallable:
        return ips_worker_fn

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        times, values, statuses, count, ptime = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())
        power, value = backdoor.power(), float('inf')

        solved = statuses.get(Status.SOLVED, 0)
        resolved = statuses.get(Status.RESOLVED, 0)
        if solved + resolved > self.min_solved * count:
            value = power * (3. * count / (solved + resolved))

        return {
            'count': count,
            'value': round(value, 2),
            'ptime': round(ptime, 4),
            'statuses': statuses,
            'time_sum': round(time_sum, 4),
            'value_sum': round(value_sum, 4),
        }


__all__ = [
    'InversePolynomialSets'
]
