import threading
from enum import Enum
from typing import List

from .contex import Context

from util.iterable import list_of
from function.model import ChunkResult, Results
from typings.error import AlreadyRunning, CancelledError
from typings.future import Future, Timeout, AcquireFutures


class JobState(Enum):
    [
        PENDING,
        RUNNING,
        FINISHED,
        CANCELLED
    ] = range(4)


DONE_STATES = [
    JobState.FINISHED,
    JobState.CANCELLED
]


class JobException(Exception):
    def __init__(self, exceptions):
        self.exceptions = exceptions


class _Waiter(object):
    def __init__(self):
        self.finished_jobs = []
        self.event = threading.Event()

    def add_result(self, job):
        self.finished_jobs.append(job)


class _NCompletedWaiter(_Waiter):
    def __init__(self, pending_calls):
        super().__init__()
        self.lock = threading.Lock()
        self.pending_calls = pending_calls

    def _decrement_pending_calls(self):
        with self.lock:
            self.pending_calls -= 1
            if not self.pending_calls:
                self.event.set()

    def add_result(self, job):
        super().add_result(job)
        self._decrement_pending_calls()


class Job(Future):
    def __init__(self, context: Context, job_id: int):
        self.job_id = job_id
        self.context = context

        self._futures = []
        self._results = []
        self._waiters = []
        self._exceptions = []
        self._state = JobState.PENDING
        self._condition = threading.Condition()
        self._job_manager = threading.Thread(
            name=f'JobManagerThread {job_id}',
            target=self._process, args=(context,)
        )

    # noinspection PyProtectedMember
    def _process(self, context: Context):
        fn = context.function.get_worker_fn()
        payload = context.function.get_payload(
            context.space, context.instance, context.searchable
        )

        tasks = context.get_tasks(self._results)
        iterables = [(args, payload) for args in tasks]
        while self.running() and len(iterables) > 0:
            future_all = context.executor.submit_all(fn, *iterables)

            is_reasonably = True
            with self._condition:
                self._futures.append(future_all)
                self._results.extend(list_of(None, iterables))

            while len(future_all) > 0 and is_reasonably:
                for future in future_all.as_complete():
                    with self._condition:
                        if future._exception is not None:
                            print(f'Worker error: {future._exception}')
                            self._exceptions.append(future._exception)
                        elif future._result is not None:
                            index = self._results.index(None)
                            result = ChunkResult(*future._result)
                            self._results[index] = result
            tasks = context.get_tasks(self._results)
            iterables = [(args, payload) for args in tasks]

        with self._condition:
            if self._state == JobState.RUNNING:
                self._state = JobState.FINISHED

            for waiter in self._waiters:
                waiter.add_result(self)
            self._condition.notify_all()

    def start(self) -> 'Job':
        if self._state != JobState.PENDING:
            raise AlreadyRunning()

        self._state = JobState.RUNNING
        self._job_manager.start()
        return self

    def cancel(self) -> bool:
        with self._condition:
            if self._state == JobState.FINISHED:
                return False

            if self._state == JobState.RUNNING:
                self._state = JobState.CANCELLED
                for future in self._futures:
                    future.cancel()
                self._condition.notify_all()

        if self._job_manager is not None:
            self._job_manager.join()
            self._job_manager = None

        return True

    def done(self) -> bool:
        with self._condition:
            return self._state in DONE_STATES

    def running(self) -> bool:
        with self._condition:
            return self._state == JobState.RUNNING

    def cancelled(self) -> bool:
        with self._condition:
            return self._state == JobState.CANCELLED

    def add_done_callback(self, fn):
        pass

    # noinspection DuplicatedCode
    def result(self, timeout: Timeout = None) -> Results:
        with self._condition:
            if self._state == JobState.CANCELLED:
                raise CancelledError()
            elif self._state == JobState.FINISHED:
                return self._results

            self._condition.wait(timeout)

            if self._state == JobState.CANCELLED:
                raise CancelledError()
            elif self._state == JobState.FINISHED:
                return self._results
            else:
                raise TimeoutError()

    # noinspection DuplicatedCode
    def exception(self, timeout: Timeout = None) -> Exception:
        with self._condition:
            if self._state == JobState.CANCELLED:
                raise CancelledError()
            elif self._state == JobState.FINISHED:
                return JobException(self._exceptions)

            self._condition.wait(timeout)

            if self._state == JobState.CANCELLED:
                raise CancelledError()
            elif self._state == JobState.FINISHED:
                return JobException(self._exceptions)
            else:
                raise TimeoutError()


# noinspection PyProtectedMember
def n_completed(jobs: List[Job], count: int, timeout: Timeout = None) -> List[Job]:
    with AcquireFutures(*jobs):
        done = set(j for j in jobs if j._state in DONE_STATES)
        not_done = set(jobs) - done
        count = min(count - len(done), len(not_done))

        if count > 0:
            waiter = _NCompletedWaiter(count)
            [j._waiters.append(waiter) for j in not_done]
        else:
            return list(done)

    waiter.event.wait(timeout)
    for job in not_done:
        with job._condition:
            job._waiters.remove(waiter)

    done.update(waiter.finished_jobs)
    return list(done)


def all_completed(jobs: List[Job], timeout: Timeout = None) -> List[Job]:
    return n_completed(jobs, len(jobs), timeout)


def first_completed(jobs: List[Job], timeout: Timeout = None) -> List[Job]:
    return n_completed(jobs, 1, timeout)


__all__ = [
    'Job',
    # waiters
    'n_completed',
    'all_completed',
    'first_completed',
]
