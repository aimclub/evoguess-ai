from typing import Tuple, TYPE_CHECKING

from ..models import WorkerCallable, Payload, \
    Results, TimeMap, ValueMap, StatusMap, Estimation

from function.module.solver import Solver
from function.module.measure import Measure
from instance.impl.instance import Instance
from instance.module.variables import Backdoor

if TYPE_CHECKING:
    from core.module.space import Space


def aggregate_results(results: Results) -> Tuple[TimeMap, ValueMap, StatusMap, int, int]:
    all_times, all_values, all_statuses, full_ptime = {}, {}, {}, 0
    for _, ptime, times, values, statuses, _ in results:
        full_ptime += ptime
        for status, time in times.items():
            all_times[status] = all_times.get(status, 0.) + time
        for status, value in values.items():
            all_values[status] = all_values.get(status, 0.) + value
        for status, count in statuses.items():
            all_statuses[status] = all_statuses.get(status, 0) + count
    return all_times, all_values, all_statuses, sum(all_statuses.values()), full_ptime


class Function:
    slug = 'function'
    supbs_required = False

    def __init__(self, solver: Solver, measure: Measure):
        self.solver = solver
        self.measure = measure

    def get_worker_fn(self) -> WorkerCallable:
        raise NotImplementedError

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        raise NotImplementedError

    def get_payload(self, space: 'Space', instance: Instance, backdoor: Backdoor) -> Payload:
        return space, self.solver, self.measure, instance, backdoor.pack()

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug,
            'solver': self.solver.__info__(),
            'measure': self.measure.__info__(),
        }


__all__ = [
    'Function',
    # utils
    'aggregate_results',
]
