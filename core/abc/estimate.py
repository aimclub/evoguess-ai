from typing import Any, Optional, Dict

from space import Space
from output import Logger
from executor import Executor
from function import Function

from ..abc.core import *
from ..model.job import Job
from ..model.handle import *
from ..model.point import Point
from ..model.contex import Context

from ..static import CORE_CACHE
from ..module.sampling import Sampling
from ..module.comparator import Comparator

from lib_satprob.problem import Problem
from typings.searchable import Searchable


class Estimate(Core):
    slug = 'core:estimate'

    def __init__(self, space: Space, logger: Logger, problem: Problem,
                 executor: Executor, sampling: Sampling, function: Function,
                 comparator: Comparator, random_seed: Optional[int] = None):
        self.space = space
        self.executor = executor
        self.sampling = sampling
        self.function = function
        self.comparator = comparator
        super().__init__(logger, problem, random_seed)

        self._job_number = 0
        CORE_CACHE.canceled = {}
        CORE_CACHE.estimated = {}
        CORE_CACHE.estimating = {}
        CORE_CACHE.best_point = None

    def launch(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def estimate(self, searchable: Searchable) -> Handle:
        if searchable in CORE_CACHE.estimating:
            # todo: refactor estimating handling
            return CORE_CACHE.estimating[searchable]

        point = Point(searchable, self.comparator)
        return self._estimate(point)

    def _estimate(self, point: Point) -> Handle:
        if point.searchable in CORE_CACHE.canceled:
            estimation = CORE_CACHE.canceled[point.searchable]
            return VoidHandle(point.set(**estimation))

        if point.searchable in CORE_CACHE.estimated:
            estimation = CORE_CACHE.estimated[point.searchable]
            return VoidHandle(point.set(**estimation))

        self._job_number += 1
        handle = JobHandle(Job(Context(
            space=self.space,
            problem=self.problem,
            function=self.function,
            sampling=self.sampling,
            executor=self.executor,
            searchable=point.searchable,
            # todo: move 2 ** 32 - 1 to const
            sample_seed=self.random_state.randint(2 ** 32 - 1)
        ), self._job_number).start(), point)
        CORE_CACHE.estimating[point.searchable] = handle

        return handle

    def __config__(self) -> Dict[str, Any]:
        # todo: add realisation
        return {}


__all__ = [
    'Estimate'
]
