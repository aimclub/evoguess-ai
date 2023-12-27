from os import getpid
from math import ceil
from time import time as now
from typing import Iterable
from numpy.random import RandomState

from lib_satprob.problem import Problem
from lib_satprob.variables import Supplements, combine

from ..model import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation
from ..abc.function import Function, aggregate_results, format_statuses

from ..module.budget import AutoBudget
from ..module.measure import Measure

from typings.searchable import Searchable


def gad_supplements(args: WorkerArgs, problem: Problem,
                    searchable: Searchable) -> Iterable[Supplements]:
    sample_seed, sample_size, offset, length = args
    sample_state = RandomState(sample_seed)

    power, substitutions = searchable.power(), []
    if problem.output_set or sample_size >= power:
        for chunk_i in range(ceil(sample_size / power)):
            output_supplements = ([], []) if not problem.output_set \
                else problem.process_output_supplements(sample_state)
            substitutions.extend([
                (supplements, output_supplements) for supplements
                in searchable.enumerate(0, power, sample_state)
            ])

        substitutions = substitutions[offset:offset + length]
        for supplements, output_supplements in substitutions:
            yield combine(supplements, output_supplements)
    else:
        dimension = searchable.dimension()
        arguments = (0, dimension, (offset + length, len(dimension)))
        for substitution in sample_state.randint(*arguments)[offset:]:
            yield searchable.substitute(using_values=substitution)


def gad_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, budget, measure, problem, bytemask = payload
    searchable, timestamp = space.unpack(bytemask), now()

    # limit = measure.get_limit(budget)
    formula = problem.encoding.get_formula(copy=False)
    statuses, times, times2, values, values2 = {}, {}, {}, {}, {}

    for supplements in gad_supplements(args, problem, searchable):
        report = problem.solver.solve(formula, supplements)
        time, value, status = measure.check_and_get(report, budget)

        times[status.value] = times.get(status.value, 0.) + time
        values[status.value] = values.get(status.value, 0.) + value
        statuses[status.value] = statuses.get(status.value, 0) + 1

        times2[status.value] = times2.get(status.value, 0.) + time ** 2
        values2[status.value] = values2.get(status.value, 0.) + value ** 2
    return getpid(), now() - timestamp, times, times2, values, values2, statuses, args


class GuessAndDetermine(Function):
    slug = 'function:gad'

    def __init__(self, budget: AutoBudget, measure: Measure):
        super().__init__(budget, measure)
        self.best_estimation = {'value': float('inf')}

    def get_worker_fn(self) -> WorkerCallable:
        return gad_worker_fn

    def calculate(self, searchable: Searchable, results: Results) -> Estimation:
        times, values, statuses, stats = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())

        power = searchable.power()
        value = value_sum if stats.count else float('inf')
        if stats.count > 0 and stats.count != power:
            value = float(value_sum) / stats.count * power

        estimation = {
            # 'power': power,
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
        if self.best_estimation['value'] > value:
            self.best_estimation = estimation
        return estimation


__all__ = [
    'GuessAndDetermine',
    # utils
    'gad_supplements',
]
