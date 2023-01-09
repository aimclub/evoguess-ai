from executor import Executor
from instance import Instance
from function import Function

from typing import List, Optional

from ..static import CORE_CACHE
from ..module.space import Space
from ..module.sampling import Sampling

from typings.optional import Int
from util.iterable import pick_by

from instance.module.variables import Backdoor
from function.models import Estimation, Results, WorkerArgs


class Context:
    def __init__(self,
                 space: Space,
                 instance: Instance,
                 function: Function,
                 sampling: Sampling,
                 executor: Executor,
                 backdoor: Backdoor,
                 sample_seed: Int):
        self.space = space
        self.backdoor = backdoor
        self.instance = instance
        self.function = function
        self.sampling = sampling
        self.executor = executor

        self.sample_seed = sample_seed
        self.sample_size = min(backdoor.power(), self.sampling.max_size) \
            if not self.instance.input_dependent else self.sampling.max_size
        self.sample_state = self.sampling.get_state(0, self.sample_size)

    def get_tasks(self, results: Results) -> List[WorkerArgs]:
        return [
            (self.sample_seed, self.sample_size, offset, length)
            for offset, length in self.sample_state.chunks(results)
        ]

    def get_estimation(self, results: Optional[Results] = None) -> Estimation:
        del CORE_CACHE.estimating[self.backdoor]
        if results is None:
            # todo: add cancel info
            estimation = CORE_CACHE.canceled[self.backdoor] = {
                'canceled': True,
                'sample_seed': self.sample_seed,
            }
        else:
            # pick it's not a pick
            picked = pick_by(results)
            if not len(picked):
                raise Exception('all workers return an error')

            estimation = CORE_CACHE.estimated[self.backdoor] = {
                'accuracy': len(picked) / len(results),
                'sample_seed': self.sample_seed,
                **self.sampling.summarize(picked),
                **self.function.calculate(self.backdoor, picked),
            }
        return estimation

    # def get_limits(self, results: Results) -> tuple[int, Optional[int]]:
    #     return 0, None
    #
    # def is_reasonably(self, futures, results: Results):
    #     return True


__all__ = [
    'Context',
]
