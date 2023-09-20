from math import ceil
from time import time as now
from typing import Tuple, List, Dict, Any, Optional

from space import Space
from output import Logger
from executor import Executor
from function import Function
from algorithm import Algorithm

from ..abc import Estimate
from ..static import CORE_CACHE
from ..model.point import PointSet
from ..model.handle import Handle, n_completed

from ..module.sampling import Sampling
from ..module.comparator import Comparator
from ..module.limitation import Limitation

from util.iterable import omit_by
from pysatmc.problem import Problem

Await = Tuple[PointSet, List[Handle]]


class Optimize(Estimate):
    slug = 'core:optimize'

    def __init__(self, space: Space, logger: Logger, problem: Problem,
                 executor: Executor, sampling: Sampling, function: Function,
                 comparator: Comparator, algorithm: Algorithm,
                 limitation: Limitation, random_seed: Optional[int] = None):
        self.algorithm = algorithm
        self.limitation = limitation
        super().__init__(space, logger, problem, executor,
                         sampling, function, comparator, random_seed)

        self.optimization_trace = []

    def launch(self, *args, **kwargs) -> PointSet:
        start_stamp = now()
        with self.logger:
            initial = self.space.get_initial(self.problem)
            self.logger.meta(initial, self.comparator)
            # todo: search root estimation in cache
            point, handles = self.estimate(initial).result(), []
            assert point.estimated(), 'initial isn\'t estimated!'
            self.logger.write((0, [point]), now() - start_stamp)
            with self.algorithm.start(point) as point_manager:
                point_chunks = self.sampling.max_chunks
                while not self.limitation.exhausted():
                    available = ceil(self.executor.free() / point_chunks)
                    handles.extend([
                        self.estimate(backdoor) for backdoor in
                        point_manager.collect(len(handles), max(0, available))
                    ])
                    estimated, handles = self._await(*handles)
                    insertion = point_manager.insert(*estimated)

                    spent_time = now() - start_stamp
                    self.logger.write(insertion, spent_time)
                    self.limitation.set('time', spent_time)
                    # self.limitation.set('iteration', insertion[0])

                [h.cancel() for h in handles]
                return point_manager.solution()

    def _await(self, *handles: Handle, count: int = 1) -> Await:
        count = count or len(handles)
        timeout = self.limitation.left('time')
        done = n_completed(handles, count, timeout)
        not_done = omit_by(handles, lambda h: h in done)
        return [h.result() for h in done], not_done

    def __config__(self) -> Dict[str, Any]:
        # todo: add realisation
        return {}


__all__ = [
    'Optimize'
]
