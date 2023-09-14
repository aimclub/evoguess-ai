from typing import Any, Dict, Optional
from numpy.random import randint, RandomState

from output import Logger
from pysatmc.problem import Problem

from ..static import DEBUGGER


class Core:
    slug = None

    def __init__(self, logger: Logger, problem: Problem,
                 random_seed: Optional[int] = None):
        self.logger = logger
        self.problem = problem

        DEBUGGER.initialize(logger)
        self.random_seed = random_seed or randint(2 ** 32 - 1)
        self.random_state = RandomState(seed=self.random_seed)

    def launch(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


__all__ = [
    'Core'
]
