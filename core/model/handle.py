from typing import Optional

from function.models import Results
from .point import Point
from .job import Job, n_completed as nc

from typings.future import Timeout
from typings.error import CancelledError


def n_completed(handles, count, timeout=None):
    done = [h for h in handles if h.done()]

    if count > len(done):
        not_done = set(handles) - set(done)
        count = min(count - len(done), len(not_done))
        jobs = nc([h.job for h in not_done], count, timeout)
        return [h for h in handles if h in done or h.job in jobs]
    else:
        return done


class Handle:
    def done(self) -> bool:
        raise NotImplementedError

    def cancel(self) -> bool:
        raise NotImplementedError

    def result(self, timeout: Timeout = None) -> Point:
        raise NotImplementedError


class JobHandle(Handle):
    def __init__(self, job: Job, point: Point):
        self.job = job
        self.point = point
        self.context = job.context

    def done(self) -> bool:
        return self.job.done()

    def cancel(self) -> bool:
        return self.job.cancel()

    def _await_results(self, timeout: Timeout) -> Optional[Results]:
        try:
            return self.job.result(timeout)
        except CancelledError:
            return None

    def result(self, timeout: Timeout = None) -> Point:
        if self.point.estimated():
            return self.point

        results = self._await_results(timeout)
        estimation = self.context.get_estimation(results)
        return self.point.set(**estimation)


class VoidHandle(Handle):
    def __init__(self, estimated: Point):
        self.estimated = estimated

    def done(self) -> bool:
        return True

    def cancel(self) -> bool:
        return False

    def result(self, timeout: Timeout = None) -> Point:
        return self.estimated


__all__ = [
    'Handle',
    'JobHandle',
    'VoidHandle',
    # waiters
    'n_completed',
]
