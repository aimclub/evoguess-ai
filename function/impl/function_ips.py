from os import getpid
from time import time as now

from ..abc.function import aggregate_results
from ..model import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation, Status
from .function_ibs import InverseBackdoorSets, ibs_supplements

from typings.searchable import Searchable


def ips_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    searchable, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    encoding_data = instance.encoding.get_data()
    with solver.use_incremental(encoding_data, measure) as incremental:
        for assumptions, _ in ibs_supplements(args, instance, searchable):
            # todo: use constraints with incremental propagation?
            time, value, status, _ = incremental.propagate(assumptions, add_model=False)

            times[status.value] = times.get(status.value, 0.) + time
            values[status.value] = values.get(status.value, 0.) + value
            statuses[status.value] = statuses.get(status.value, 0) + 1
    return getpid(), now() - timestamp, times, values, statuses, args


class InversePolynomialSets(InverseBackdoorSets):
    slug = 'function:ips'

    def get_worker_fn(self) -> WorkerCallable:
        return ips_worker_fn

    def calculate(self, searchable: Searchable, results: Results) -> Estimation:
        times, values, statuses, count, ptime = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())
        power, value = searchable.power(), float('inf')

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
