from os import getpid
from math import ceil
from time import time as now
from pysat.solvers import Glucose3
from numpy.random import RandomState
from typing import Callable, Iterable, List

from ..models import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation
from ..abc.function import Function, aggregate_results

from util.iterable import concat
from instance.impl.instance import Instance
from instance.module.variables import Backdoor
from instance.module.variables.vars import Supplements, compress


def sequence_mapper(var_bases: List[int]) -> Callable:
    reversed_var_bases = var_bases[::-1]

    def map_substitution(number: int) -> List[int]:
        substitution = []
        for base in reversed_var_bases:
            number, value = divmod(number, base)
            substitution.insert(0, value)
        return substitution

    return map_substitution


def gad_supplements(args: WorkerArgs, instance: Instance,
                    backdoor: Backdoor) -> Iterable[Supplements]:
    sample_seed, sample_size, offset, length = args
    sample_state = RandomState(sample_seed)
    var_bases = backdoor.get_var_bases()
    var_power = backdoor.power()

    if sample_size >= var_power:
        sequence = concat(*(
            sample_state.permutation(var_power)
            for _ in range(ceil(sample_size / var_power))
        ))[offset:offset + length]
        substitutions = list(map(sequence_mapper(var_bases), sequence))
    else:
        shape = (offset + length, len(var_bases))
        substitutions = sample_state.randint(0, var_bases, shape)[offset:]

    if instance.input_dependent:
        encoding_data = instance.encoding.get_data()
        instance_vars = instance.get_instance_vars()
        # todo: use solver.DEFAULT instead of Glucose3
        # todo: improve function package typing
        with Glucose3(encoding_data.clauses()) as solver:
            for substitution in substitutions:
                values = {var: value for var, value in zip(backdoor, substitution)}
                assumptions, _ = instance_vars.get_propagation(sample_state)
                yield compress(
                    *(var.supplements(values) for var in backdoor),
                    instance_vars.get_dependent(solver.propagate(assumptions)[1])
                )
    else:
        for substitution in substitutions:
            values = {var: value for var, value in zip(backdoor, substitution)}
            yield compress(*(var.supplements(values) for var in backdoor))


def gad_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    backdoor, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    encoding_data = instance.encoding.get_data()
    for supplements in gad_supplements(args, instance, backdoor):
        time, value, status, _ = solver.solve(
            encoding_data, measure, supplements, add_model=False
        )
        times[status.value] = times.get(status.value, 0.) + time
        values[status.value] = values.get(status.value, 0.) + value
        statuses[status.value] = statuses.get(status.value, 0) + 1
    return getpid(), now() - timestamp, times, values, statuses, args


class GuessAndDetermine(Function):
    slug = 'function:gad'

    def get_worker_fn(self) -> WorkerCallable:
        return gad_worker_fn

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        times, values, statuses, count, ptime = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())
        power, value = backdoor.power(), value_sum if count else None

        if count > 0 and count != power:
            value = float(value_sum) / count * power

        return {
            'count': count,
            'value': round(value, 2),
            'ptime': round(ptime, 4),
            'statuses': statuses,
            'time_sum': round(time_sum, 4),
            'value_sum': round(value_sum, 4),
        }


__all__ = [
    'GuessAndDetermine',
    # utils
    'gad_supplements',
    'sequence_mapper'
]
