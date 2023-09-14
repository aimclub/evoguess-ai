from typing import Tuple, NamedTuple, Dict

from space import Space
from pysatmc.problem import Problem

from ..model import WorkerCallable, Payload, Results, \
    Status, TimeMap, ValueMap, StatusMap, Estimation

from ..module.budget import Budget
from ..module.measure import Measure

from typings.searchable import Searchable


class ResultsStat(NamedTuple):
    count: int
    time_avg: float
    time_var: float
    value_avg: float
    value_var: float
    ptime_sum: float


AggregatedResults = Tuple[TimeMap, ValueMap, StatusMap, ResultsStat]


def format_statuses(statuses: StatusMap) -> Dict[str, int]:
    return {Status(key).name: value for key, value in statuses.items()}


def aggregate_results(results: Results) -> AggregatedResults:
    sum_times2, sum_values2 = 0., 0.
    sum_count, sum_times, sum_values = 0, 0., 0.
    all_times, all_values, all_statuses, sum_ptime = {}, {}, {}, 0.
    for _, ptime, times, times2, values, values2, statuses, _ in results:
        sum_ptime += ptime
        sum_times2 += sum(times2.values())
        sum_values2 += sum(values2.values())

        for status, time in times.items():
            sum_times += time
            all_times[status] = all_times.get(status, 0.) + time
        for status, value in values.items():
            sum_values += value
            all_values[status] = all_values.get(status, 0.) + value
        for status, count in statuses.items():
            sum_count += count
            all_statuses[status] = all_statuses.get(status, 0) + count

    if sum_count > 0:
        time_avg = sum_times / sum_count
        value_avg = sum_values / sum_count
        time_var = sum_times2 / sum_count - time_avg ** 2
        value_var = sum_values2 / sum_count - value_avg ** 2
    else:
        time_avg, value_avg = 0., 0.
        time_var, value_var = 0., 0.
    return all_times, all_values, all_statuses, ResultsStat(
        sum_count, time_avg, time_var, value_avg, value_var, sum_ptime
    )


class Function:
    slug = 'function'
    supbs_required = False

    def __init__(self, budget: Budget, measure: Measure):
        self.budget, self.measure = budget, measure

    def get_worker_fn(self) -> WorkerCallable:
        raise NotImplementedError

    def calculate(self, searchable: Searchable,
                  results: Results) -> Estimation:
        raise NotImplementedError

    def get_payload(self, space: Space, problem: Problem,
                    searchable: Searchable) -> Payload:
        return space, self.budget, self.measure, problem, searchable.pack()

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug,
            'measure': self.measure.__info__(),
        }


__all__ = [
    'Function',
    # utils
    'format_statuses',
    'aggregate_results',
]
