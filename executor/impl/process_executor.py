from os import cpu_count
from concurrent.futures import ProcessPoolExecutor

from ..abc.executor import *


class ProcessExecutor(Executor):
    slug = 'executor:process'

    def __init__(self, max_workers: int = None):
        super().__init__(max_workers or cpu_count())
        self.executor = ProcessPoolExecutor(max_workers=self.max_workers)

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True):
        self.executor.shutdown(wait)


__all__ = [
    'ProcessExecutor'
]
