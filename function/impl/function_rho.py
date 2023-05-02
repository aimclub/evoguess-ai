from os import getpid
from time import time as now

from ..abc.function import aggregate_results
from ..model import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation, Status
from .function_gad import GuessAndDetermine, gad_supplements

from typings.searchable import Searchable
from function.module.solver import Solver
from function.module.measure import Measure


def rho_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    searchable, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    encoding_data = instance.encoding.get_data()
    with solver.use_incremental(encoding_data, measure) as incremental:
        for assumptions, _ in gad_supplements(args, instance, searchable):
            # todo: use constraints with incremental propagation?
            time, value, status, _ = incremental.propagate(assumptions, add_model=False)

            times[status.value] = times.get(status.value, 0.) + time
            values[status.value] = values.get(status.value, 0.) + value
            statuses[status.value] = statuses.get(status.value, 0) + 1
    return getpid(), now() - timestamp, times, values, statuses, args


class RhoFunction(GuessAndDetermine):
    slug = 'function:rho'

    def __init__(self, solver: Solver, measure: Measure, penalty_power: float):
        super().__init__(solver, measure)
        self.penalty_power = penalty_power

    def get_worker_fn(self) -> WorkerCallable:
        return rho_worker_fn

    def calculate(self, searchable: Searchable, results: Results) -> Estimation:
        times, values, statuses, count, ptime = aggregate_results(results)
        power, time_sum = searchable.power(), sum(times.values())

        if count > 0 and self.penalty_power > power:
            rho_value = float(statuses.get(Status.RESOLVED, 0)) / count
            penalty_value = (1. - rho_value) * self.penalty_power
            value = rho_value * power + penalty_value
        else:
            value = float('inf')

        return {
            'count': count,
            'value': round(value, 6),
            'ptime': round(ptime, 4),
            'statuses': statuses,
            'time_sum': round(time_sum, 4),
        }


__all__ = [
    'RhoFunction'
]
