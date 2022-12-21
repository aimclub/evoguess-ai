from typing import Any

from output import Logger
from executor import Executor
from function import Function
from instance import Instance

from ..abc.core import *
from ..model.job import Job
from ..model.handle import *
from ..model.point import Point
from ..model.contex import Context

from ..static import CORE_CACHE
from ..module.space import Space
from ..module.sampling import Sampling
from ..module.comparator import Comparator

from typings.optional import Int
from instance.module.variables import Backdoor


class Estimate(Core):
    slug = 'core:estimate'

    def __init__(self,
                 space: Space,
                 logger: Logger,
                 instance: Instance,
                 executor: Executor,
                 sampling: Sampling,
                 function: Function,
                 comparator: Comparator,
                 random_seed: Int = None):
        self.space = space
        self.executor = executor
        self.sampling = sampling
        self.function = function
        self.comparator = comparator
        super().__init__(logger, instance, random_seed)

        self._job_number = 0
        CORE_CACHE.canceled = {}
        CORE_CACHE.estimated = {}
        CORE_CACHE.estimating = {}

    def launch(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def estimate(self, backdoor: Backdoor) -> Handle:
        if backdoor in CORE_CACHE.estimating:
            # todo: refactor estimating handling
            return CORE_CACHE.estimating[backdoor]

        point = Point(backdoor, self.comparator)
        return self._estimate(point)

    def _estimate(self, point: Point) -> Handle:
        if point.backdoor in CORE_CACHE.canceled:
            estimation = CORE_CACHE.canceled[point.backdoor]
            return VoidHandle(point.set(**estimation))

        if point.backdoor in CORE_CACHE.estimated:
            estimation = CORE_CACHE.estimated[point.backdoor]
            return VoidHandle(point.set(**estimation))

        self._job_number += 1
        handle = JobHandle(Job(Context(
            space=self.space,
            instance=self.instance,
            function=self.function,
            sampling=self.sampling,
            executor=self.executor,
            backdoor=point.backdoor,
            # todo: move 2 ** 32 - 1 to const
            sample_seed=self.random_state.randint(2 ** 32 - 1)
        ), self._job_number).start(), point)
        CORE_CACHE.estimating[point.backdoor] = handle

        return handle


__all__ = [
    'Estimate'
]
