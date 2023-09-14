from space import Space
from executor import Executor
from function import Function

from typing import List, Optional
from util.iterable import pick_by

from ..static import CORE_CACHE
from ..module.sampling import Sampling

from pysatmc.problem import Problem
from typings.searchable import Searchable
from function.model import Estimation, Results, WorkerArgs


class Context:
    def __init__(
            self,
            space: Space,
            problem: Problem,
            function: Function,
            sampling: Sampling,
            executor: Executor,
            searchable: Searchable,
            sample_seed: Optional[int]
    ):
        self.space = space
        self.problem = problem
        self.function = function
        self.sampling = sampling
        self.executor = executor
        self.searchable = searchable

        self.sample_seed = sample_seed
        self.sample_size = min(searchable.power(), self.sampling.max_size) \
            if not self.problem.output_set else self.sampling.max_size
        self.sample_state = self.sampling.get_state(0, self.sample_size)

    def get_tasks(self, results: Results) -> List[WorkerArgs]:
        return [
            (self.sample_seed, self.sample_size, offset, length)
            for offset, length in self.sample_state.chunks(results)
        ]

    def get_estimation(self, results: Optional[Results] = None) -> Estimation:
        del CORE_CACHE.estimating[self.searchable]
        if results is None:
            # todo: add cancel info
            estimation = CORE_CACHE.canceled[self.searchable] = {
                'canceled': True,
                'sample_seed': self.sample_seed,
            }
        else:
            # pick it's not a pick
            picked = pick_by(results)
            if not len(picked):
                raise Exception('all workers return an error')

            estimation = CORE_CACHE.estimated[self.searchable] = {
                'accuracy': len(picked) / len(results),
                'sample_seed': self.sample_seed,
                **self.sampling.summarize(picked),
                **self.function.calculate(self.searchable, picked),
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
