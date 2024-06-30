import os

from time import time
from itertools import chain
from threading import Event, Lock
from concurrent.futures import Future
from typing import List, Tuple, Iterable, Callable

from space import Space
from core.model.point import Point

from .operator.selection import Selection

from lib_metalg.function import Function
from lib_metalg.algorithm import Iteration, Island
from lib_metalg.condition import Condition, EmptyCond


class Result:
    def __init__(
            self,
            name: str,
            futures: List[Future]
    ):
        self.name = name
        self.futures = futures


class _AcquireFutures(object):
    def __init__(self, futures):
        self.futures = sorted(futures, key=id)

    def __enter__(self):
        for future in self.futures:
            future._condition.acquire()

    def __exit__(self, *args):
        for future in self.futures:
            future._condition.release()


class _CallbackWaiter:
    def __init__(self, callback):
        self.lock = Lock()
        self.event = Event()
        self.callback = callback

    def add_result(self, future):
        with self.lock:
            if self.callback(future):
                self.event.set()

    def add_exception(self, future):
        with self.lock:
            if self.callback(future):
                self.event.set()

    def add_cancelled(self, future):
        with self.lock:
            if self.callback(future):
                self.event.set()


def wait_its(
        iterations: List[Iteration],
        stop_cond: Condition,
        max_workers: int
) -> [List[Result], List[Iteration]]:
    results, pending = [], {}
    it_map, pending_map = {}, {}
    futures, future_map = [], {}
    for iteration in iterations:
        for future in iteration.next:
            key = hash(future)
            futures.append(future)
            if key not in future_map:
                future_map[key] = []
            future_map[key].append(
                iteration.name
            )
            pending[key] = True

        it_map[iteration.name] = []
        pending_map[iteration.name] = len(iteration.next)

    def add_to_finished(_future: Future):
        _key, _flag = hash(_future), False
        for _name in future_map[_key]:
            it_map[_name].append(_future)
            pending_map[_name] -= 1
            del pending[_key]

        return len(pending) <= max_workers

    def update_results():
        for _name in list(it_map.keys()):
            if pending_map[_name] <= 0:
                _futures = it_map[_name]
                results.append(Result(
                    _name, _futures
                ))
                del it_map[_name]

    futures = set(futures)
    with _AcquireFutures(futures):
        not_done = set()
        for future in futures:
            if future._state == 'FINISHED':
                add_to_finished(future)
            else:
                not_done.add(future)

        update_results()
        if len(results) > 0:
            return results, [
                it for it in iterations
                if it.name in it_map
            ]

        waiter = _CallbackWaiter(add_to_finished)
        for future in not_done:
            future._waiters.append(waiter)

    waiter.event.wait()
    for future in not_done:
        with future._condition:
            future._waiters.remove(waiter)

    update_results()
    return results, [
        it for it in iterations
        if it.name in it_map
    ]


class PointCollector:
    _point_count = 0

    def __init__(
            self,
            capacity: int,
            diversity: int,
            max_value: float,
            callback: Callable,
    ):
        self._storage = {}
        self._point_set = set()
        self._capacity = capacity
        self._callback = callback
        self._diversity = diversity
        self._max_value = max_value
        self.__max_value = max_value

    def get(self) -> Iterable[Point]:
        return chain(*self._storage.values())

    def add(self, point: Point):
        value = point.value()
        if value > self.__max_value:
            return

        if value not in self._storage:
            keys = self._storage.keys()
            if len(keys) < self._diversity:
                self._point_set.add(point.searchable)
                self._storage[value] = [point]
                self._point_count += 1
                if self._callback:
                    self._callback(1)
            elif max(keys) > value:
                points = self._storage[max(keys)]
                self._point_count -= len(points)
                if self._callback:
                    self._callback(-len(points))
                del self._storage[max(keys)]

                self._point_set.add(point.searchable)
                self._storage[value] = [point]
                self.__max_value = max(keys)
                self._point_count += 1
                if self._callback:
                    self._callback(1)
        elif point.searchable not in self._point_set:
            self._point_set.add(point.searchable)
            self._storage[value].append(point)
            self._point_count += 1
            if self._callback:
                self._callback(1)

    def is_filled(self) -> bool:
        return self._point_count >= self._capacity


class NotUniqueNameException(Exception):
    def __init__(self, name: str):
        super().__init__(name)


def not_unique(name: str):
    raise NotUniqueNameException(name)


def unpack(
        results: List[Result]
) -> List[Tuple[str, List[Point]]]:
    return [
        (result.name, [
            f.result() for f
            in result.futures
        ]) for result in results
    ]


class Migration:
    def __init__(
            self,
            sender: Island,
            receiver: Island,
            selection: Selection,
            send_cond: Condition,
    ):
        self.sender = sender
        self.receiver = receiver
        self.selection = selection
        self.send_cond = send_cond

    def migrate(self, iteration: Iteration):
        stats = self.sender.stats
        if self.send_cond.reached(stats):
            points = self.selection.select(
                iteration.current, 1
            )
            self.send_cond.move(stats)
            self.receiver.receive(points)


class Ocean:
    stats = None

    def __init__(
            self,
            function: Function,
            islands: List[Island],
            topology: List[Migration],
            collector: PointCollector,
    ):
        names = set()
        for island in islands:
            if island.name in names:
                not_unique(island.name)
            names.add(island.name)

        self.islands = {
            island.name: island
            for island in islands
        }
        self.topology = {
            name: [] for name in
            self.islands.keys()
        }
        self.function = function
        self.collector = collector

        for edge in topology:
            name = edge.sender.name
            edges = self.topology.get(name)
            if edges is not None:
                edges.append(edge)

    def launch(
            self,
            space: Space,
            stop_cond: Condition = None,
    ) -> Iterable[Point]:
        stamp, iterations = time(), [
            island.start(space, self.function)
            for island in self.islands.values()
        ]

        def _get_log_file() -> str:
            cap = f'cap={self.collector._capacity}'
            div = f'div={self.collector._diversity}'
            _mx = f'max={self.collector._max_value}'
            _run = f'{cap}_{div}_{_mx}'

            problem = self.function._problem
            key = problem.encoding._reader.from_file
            return f'{key.split("/")[-1]}_{_run}.log'

        log_file = _get_log_file()
        if os.path.exists(log_file):
            os.remove(log_file)

        cycles, cycle_mod = 0, 25 * len(self.islands)
        while not self.collector.is_filled():
            results, iterations = wait_its(
                iterations, stop_cond,
                self.function.max_workers
            )

            for name, points in unpack(results):
                island = self.islands[name]
                iteration = island.process(points)
                iterations.append(iteration)

                for edge in self.topology[name]:
                    edge.migrate(iteration)

                for point in iteration.current:
                    self.collector.add(point)

                if cycles % cycle_mod == 0:
                    indexes = []
                    for pl in self.collector._storage.values():
                        for point in pl:
                            _vars = point.searchable.variables()
                            indexes.extend(v.index for v in _vars)

                    log_file = _get_log_file()
                    with open(log_file, 'a+') as handle:
                        print(
                            self.collector._point_count,
                            self.collector._storage.keys(),
                            island.stats, len(indexes), '->',
                            len(set(indexes)), file=handle
                        )
                cycles += 1

        indexes = []
        for pl in self.collector._storage.values():
            for point in pl:
                _vars = point.searchable.variables()
                indexes.extend(v.index for v in _vars)

        log_file = _get_log_file()
        with open(log_file, 'a+') as handle:
            print(
                self.collector._point_count,
                self.collector._storage.keys(),
                list(self.islands.values())[-1].stats,
                len(indexes), '->', len(set(indexes)),
                file=handle
            )

        yield from self.collector.get()


__all__ = [
    'Ocean',
    'Migration',
    # utility
    'PointCollector'
]

