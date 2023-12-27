from os import getpid
from time import time as now

from ..model import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation, Status
from ..abc.function import aggregate_results, format_statuses
from .function_ibs import InverseBackdoorSets, ibs_supplements

from ..module.measure import Measure
from ..module.budget import TaskBudget

from typings.searchable import Searchable


def ips_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, budget, measure, problem, bytemask = payload
    searchable, timestamp = space.unpack(bytemask), now()

    formula = problem.encoding.get_formula(copy=False)
    statuses, times, times2, values, values2 = {}, {}, {}, {}, {}

    with problem.solver.get_instance(formula) as incremental:
        for supplements in ibs_supplements(args, problem, searchable):
            report = incremental.propagate(supplements)
            time, value, status = measure.check_and_get(report, budget)

            times[status.value] = times.get(status.value, 0.) + time
            values[status.value] = values.get(status.value, 0.) + value
            statuses[status.value] = statuses.get(status.value, 0) + 1

            times2[status.value] = times2.get(status.value, 0.) + time ** 2
            values2[status.value] = values2.get(status.value, 0.) + value ** 2
    return getpid(), now() - timestamp, times, times2, values, values2, statuses, args


class InversePolynomialSets(InverseBackdoorSets):
    slug = 'function:ips'

    def __init__(self, measure: Measure, min_solved: float = 0.,
                 only_propagate: bool = False):
        super().__init__(TaskBudget(0), measure, min_solved)
        self.only_propagate = only_propagate

    def get_worker_fn(self) -> WorkerCallable:
        return ips_worker_fn

    def calculate(self, searchable: Searchable, results: Results) -> Estimation:
        times, values, statuses, stats = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())
        power, value = searchable.power(), float('inf')

        solved = statuses.get(Status.RESOLVED, 0) + (
            0 if self.only_propagate else
            statuses.get(Status.SOLVED, 0)
        )
        if solved > 0 and solved >= self.min_solved * stats.count:
            value = power * (3. * stats.count / solved)

        return {
            'count': stats.count,
            'value': round(value, 2),
            'ptime': round(stats.ptime_sum, 4),
            'time_sum': round(time_sum, 4),
            'time_avg': round(stats.time_avg, 6),
            'time_var': round(stats.time_var, 6),
            'statuses': format_statuses(statuses),
            'value_sum': round(value_sum, 4),
            'value_avg': round(stats.value_avg, 6),
            'value_var': round(stats.value_var, 6),
        }


__all__ = [
    'InversePolynomialSets'
]
