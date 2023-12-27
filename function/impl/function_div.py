from os import getpid
from time import time as now

from util.iterable import list_of
from ..model import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation
from .function_gad import GuessAndDetermine, gad_supplements
from ..abc.function import aggregate_results, format_statuses

from ..module.budget import AutoBudget
from ..module.measure import SolvingTime

from typings.searchable import Searchable


def div_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, budget, measure, problem, bytemask = payload
    searchable, timestamp = space.unpack(bytemask), now()

    _formula = problem.encoding.get_formula(copy=False)
    statuses, times, times2, values, values2 = {}, {}, {}, {}, {}

    hard, soft, vector = [], [], searchable.get_vector()
    for bit, clause in zip(vector, _formula.clauses):
        (hard if bit else soft).append(clause)

    # todo: optimize
    formula = _formula.weighted()
    formula.wght = list_of(1, soft)
    formula.topw = len(soft) + 1
    formula.hard = hard
    formula.soft = soft

    for supplements in gad_supplements(args, problem, searchable):
        report = problem.solver.solve(formula, supplements)
        time, value, status = measure.check_and_get(report, budget)

        times[status.value] = times.get(status.value, 0.) + time
        values[status.value] = values.get(status.value, 0.) + value
        statuses[status.value] = statuses.get(status.value, 0) + 1

        times2[status.value] = times2.get(status.value, 0.) + time ** 2
        values2[status.value] = values2.get(status.value, 0.) + value ** 2
    return getpid(), now() - timestamp, times, times2, values, values2, statuses, args


class DivFunction(GuessAndDetermine):
    slug = 'function:div'

    def __init__(self, budget: AutoBudget):
        super().__init__(budget, SolvingTime())

    def get_worker_fn(self) -> WorkerCallable:
        return div_worker_fn

    def calculate(self, searchable: Searchable, results: Results) -> Estimation:
        times, values, statuses, stats = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())

        power = searchable.power()
        value = value_sum if stats.count else float('inf')
        if stats.count > 0 and stats.count != power:
            value = float(value_sum) / stats.count * power

        return {
            'power': power,
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
    'DivFunction'
]
