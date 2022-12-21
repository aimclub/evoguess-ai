import time
import threading

from typing import List
from typings.optional import Int, Float
from typings.future import Future, AcquireFutures

NOTIFIED_STATES = [
    'FINISHED',
    'CANCELLED_AND_NOTIFIED'
]


class _Tracker:
    # noinspection PyProtectedMember
    def __init__(self, futures):
        self.event = None
        self.pending_calls = 0
        self.finished_futures = []
        self.lock = threading.Lock()

        with AcquireFutures(*futures):
            self.pending_futures = 0
            for future in futures:
                if future._state in NOTIFIED_STATES:
                    self.finished_futures.append(future)
                else:
                    self.pending_futures += 1
                    future._waiters.append(self)

    def _decrement_pending_calls(self):
        if self.event:
            self.pending_calls -= 1
            if not self.pending_calls:
                self.event.set()

    def add_result(self, future):
        with self.lock:
            self.pending_futures -= 1
            self._decrement_pending_calls()
            self.finished_futures.append(future)

    def add_exception(self, future):
        with self.lock:
            self.pending_futures -= 1
            self._decrement_pending_calls()
            self.finished_futures.append(future)

    def add_cancelled(self, future):
        with self.lock:
            self.pending_futures -= 1
            self._decrement_pending_calls()
            self.finished_futures.append(future)


# noinspection PyProtectedMember
class FutureAll:
    def __init__(self, futures: List[Future]):
        self._futures = set(futures)
        self._tracker = _Tracker(futures)

        # print(f'-- create <FutureAll-{id(self)}> of {len(futures)} futures')

    def _release_futures(self) -> List[Future]:
        with self._tracker.lock:
            finished = self._tracker.finished_futures
            self._tracker.finished_futures = []
            self._tracker.event = None
        self._futures -= set(finished)

        # print(f'-- release <FutureAll-{id(self)}> of {len(finished)} futures')
        for future in finished:
            if self._tracker in future._waiters:
                with future._condition:
                    future._waiters.remove(self._tracker)
        return finished

    # noinspection PyProtectedMember
    def as_complete(self, count: Int = None, timeout: Float = None) -> List[Future]:
        assert self._tracker.event is None, "not thread safety!"
        assert count is None or count >= 0, "not uint!"

        if timeout is not None:
            if timeout <= 0:
                return self._release_futures()
            end_time = timeout + time.time()

        count = count or len(self._futures)
        with self._tracker.lock:
            if count > len(self._tracker.finished_futures):
                self._tracker.event = threading.Event()
                self._tracker.pending_calls = min(
                    self._tracker.pending_futures,
                    count - len(self._tracker.finished_futures)
                )

        if self._tracker.event:
            if timeout is not None:
                timeout = end_time - time.time()
            self._tracker.event.wait(timeout)

        return self._release_futures()

    def cancel(self) -> float:
        canceled = 0.
        for future in self._futures:
            canceled += int(future.cancel())
        return canceled / len(self._futures)

    def append_tracker_to(self, trackers: List[_Tracker]) -> 'FutureAll':
        trackers.append(self._tracker)
        return self

    @property
    def pending_futures(self) -> int:
        return self._tracker.pending_futures

    def __len__(self):
        return len(self._futures)


__all__ = [
    'FutureAll'
]
