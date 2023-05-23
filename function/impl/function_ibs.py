from os import getpid
from typing import Iterable
from time import time as now
from pysat.solvers import Glucose3
from numpy.random import RandomState

from instance import Instance

from ..model import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation, Status
from ..abc.function import Function, aggregate_results, format_statuses

from ..module.solver import Solver
from ..module.measure import Measure

from function.module.budget.impl import TaskBudget
from typings.searchable import Searchable, Supplements


def ibs_supplements(args: WorkerArgs, instance: Instance,
                    searchable: Searchable) -> Iterable[Supplements]:
    # IBS function works only with input dependent formulas
    if not instance.input_dependent: return ()

    sample_seed, _, offset, length = args
    sample_state = RandomState(sample_seed)
    encoding_data = instance.encoding.get_data()
    instance_vars = instance.get_instance_vars(searchable)
    # todo: use solver.DEFAULT instead of Glucose3
    # todo: improve function package typing
    with Glucose3(encoding_data.clauses()) as solver:
        for index in range(offset + length):
            assumptions, _ = instance_vars.get_propagation(sample_state)
            if index >= offset:
                yield instance_vars.get_dependent(solver.propagate(assumptions)[1])


def ibs_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, budget, measure, instance, bytemask = payload
    backdoor, timestamp = space.unpack(instance, bytemask), now()

    limit = measure.get_limit(budget)
    times, times2, values, values2 = {}, {}, {}, {}
    encoding_data, statuses = instance.encoding.get_data(), {}
    for supplements in ibs_supplements(args, instance, backdoor):
        report = solver.solve(encoding_data, supplements, limit)
        time, value, status = measure.check_and_get(report, budget)

        times[status.value] = times.get(status.value, 0.) + time
        values[status.value] = values.get(status.value, 0.) + value
        statuses[status.value] = statuses.get(status.value, 0) + 1

        times2[status.value] = times2.get(status.value, 0.) + time ** 2
        values2[status.value] = values2.get(status.value, 0.) + value ** 2
    return getpid(), now() - timestamp, times, times2, values, values2, statuses, args


class InverseBackdoorSets(Function):
    slug = 'function:ibs'
    supbs_required = True

    def __init__(self, solver: Solver, budget: TaskBudget,
                 measure: Measure, min_solved: float = 0.):
        super().__init__(solver, budget, measure)
        self.min_solved = min_solved

    def get_worker_fn(self) -> WorkerCallable:
        return ibs_worker_fn

    def calculate(self, searchable: Searchable, results: Results) -> Estimation:
        times, values, statuses, stats = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())
        power, budget, value = searchable.power(), self.budget.value(), float('inf')

        resolved = statuses.get(Status.RESOLVED, 0)
        if resolved > 0 and resolved >= self.min_solved * stats.count:
            value = power * budget * (3. * stats.count / resolved)

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
    'InverseBackdoorSets',
    # utils
    'ibs_supplements'
]
