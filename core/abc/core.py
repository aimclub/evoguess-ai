from typing import Any, Dict

from output import Logger
from instance import Instance

from ..static import DEBUGGER

from typings.optional import Int
from numpy.random import randint, RandomState


class Core:
    slug = None

    def __init__(self,
                 logger: Logger,
                 instance: Instance,
                 random_seed: Int = None):
        self.logger = logger
        self.instance = instance

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
