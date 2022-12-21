from typing import Any
from typings.optional import Int

Timeout = Int


class Future:
    def cancel(self) -> bool:
        raise NotImplementedError

    def done(self) -> bool:
        raise NotImplementedError

    def running(self) -> bool:
        raise NotImplementedError

    def cancelled(self) -> bool:
        raise NotImplementedError

    def add_done_callback(self, fn):
        raise NotImplementedError

    def result(self, timeout: Timeout = None) -> Any:
        raise NotImplementedError

    def exception(self, timeout: Timeout = None) -> Exception:
        raise NotImplementedError


# noinspection PyProtectedMember
class AcquireFutures(object):
    def __init__(self, *futures: Future):
        self.futures = sorted(futures, key=id)

    def __enter__(self):
        for future in self.futures:
            future._condition.acquire()

    def __exit__(self, *args):
        for future in self.futures:
            future._condition.release()


__all__ = [
    'Future',
    'Timeout',
    'AcquireFutures'
]
