from os import getpid
from time import time as now

from ..model import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation, Status
from ..abc.function import aggregate_results, format_statuses
from .function_gad import GuessAndDetermine, gad_supplements

from ..module.measure import Measure
from ..module.budget import AutoBudget

from typings.searchable import Searchable


def rho_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, budget, measure, problem, bytemask = payload
    searchable, timestamp = space.unpack(bytemask), now()

    times, times2, values, values2 = {}, {}, {}, {}
    formula, statuses = problem.encoding.get_formula(), {}
    with problem.solver.get_instance(formula) as incremental:
        for supplements in gad_supplements(args, problem, searchable):
            report = incremental.propagate(supplements)
            time, value, status = measure.check_and_get(report, budget)

            times[status.value] = times.get(status.value, 0.) + time
            values[status.value] = values.get(status.value, 0.) + value
            statuses[status.value] = statuses.get(status.value, 0) + 1

            times2[status.value] = times2.get(status.value, 0.) + time ** 2
            values2[status.value] = values2.get(status.value, 0.) + value ** 2
    return getpid(), now() - timestamp, times, times2, values, values2, statuses, args


class RhoFunction(GuessAndDetermine):
    slug = 'function:rho'

    def __init__(self, measure: Measure, penalty_power: float,
                 only_solved: bool = False):
        super().__init__(AutoBudget(), measure)
        self.penalty_power = penalty_power
        self.only_solved = only_solved

    def get_worker_fn(self) -> WorkerCallable:
        return rho_worker_fn

    def calculate(self, searchable: Searchable, results: Results) -> Estimation:
        times, values, statuses, stats = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())
        power, value = searchable.power(), float('inf')

        solved = statuses.get(Status.SOLVED, 0) + (
            statuses.get(Status.RESOLVED, 0)
            if not self.only_solved else 0
        )
        if stats.count > 0 and self.penalty_power > power:
            rho_value = float(solved) / stats.count
            penalty_value = (1. - rho_value) * self.penalty_power
            value = rho_value * power + penalty_value

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
    'RhoFunction'
]
