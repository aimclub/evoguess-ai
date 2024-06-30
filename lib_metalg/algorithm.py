from time import time
from uuid import uuid4
from itertools import chain
from concurrent.futures import Future, wait
from typing import List, Iterable, NamedTuple

from core.model.point import Point
from utility.iterable import slice_by
from typings.searchable import Searchable

from space import Space
from .function import Function
from .condition import Stats, Condition, EmptyCond

from .operator.mutation import Mutation
from .operator.crossover import Crossover
from .operator.selection import Selection


class Iteration(NamedTuple):
    name: str
    index: int
    next: List[Future]
    current: List[Point]


def _get_name() -> str:
    return uuid4().hex


class Island:
    space = None
    stats = None
    function = None

    def __init__(self, name: str = None):
        self.name = name or _get_name()
        self.migrated = []

    def start(
            self,
            space: Space,
            function: Function,
    ) -> Iteration:
        self.space = space
        self.stats = Stats()
        self.function = function
        initial = space.get_initial()
        self.stats.set('stamp', time())
        return Iteration(self.name, 0, [
            function.evaluate(initial)
        ], [])

    def receive(
            self,
            points: List[Point]
    ):
        self.migrated.extend(points)

    def process(
            self,
            points: List[Point]
    ) -> Iteration:
        raise NotImplementedError

    @property
    def solution(self) -> Point:
        raise NotImplementedError


class Algorithm(Island):
    def __init__(
            self,
            island_name: str = None,
            restart_cond: Condition = None
    ):
        super().__init__(island_name)
        self.restart_solutions = []
        self.restart_cond = restart_cond or EmptyCond()

    def optimize(
            self,
            space: Space,
            function: Function,
            stop_cond: Condition = None
    ) -> Iterable[Iteration]:
        stop_cond = stop_cond or EmptyCond()
        iteration = self.start(space, function)
        while not stop_cond.reached(self.stats):
            done, _ = wait(
                iteration.next,
                stop_cond.left(self.stats)
            )
            iteration = self.process([
                f.result() for f in done
            ], stop_cond.reached(self.stats))

            yield iteration

    def process(
            self,
            points: List[Point],
            stopping: bool = False
    ) -> Iteration:
        restarting = False
        searchables = self.iterate(
            [*points, *self.migrated]
        )
        self.migrated = []
        index = self.stats.increase('iter')
        current_state = self.current_state
        if stopping: return Iteration(
            self.name, index, [], current_state
        )

        if self.restart_cond.reached(self.stats):
            solution = current_state[0]
            self.stats.increase('restarts')
            self.restart_cond.move(self.stats)
            self.restart_solutions.append(solution)
            initial = self.space.get_initial()
            searchables = [initial]
            self.reset_state()

        return Iteration(self.name, index, [
            self.function.evaluate(searchable)
            for searchable in searchables
        ], current_state)

    def iterate(
            self,
            points: List[Point]
    ) -> List[Searchable]:
        raise NotImplementedError

    @property
    def solution(self) -> Point:
        return min(
            self.current_state[0],
            *self.restart_solutions,
        )

    @property
    def current_state(self) -> List[Point]:
        raise NotImplementedError

    def reset_state(self):
        raise NotImplementedError


class Evolution(Algorithm):
    tweak_size = None

    def __init__(
            self,
            mutation: Mutation,
            selection: Selection,
            island_name: str = None,
            restart_cond: Condition = None
    ):
        self.mutation = mutation
        self.selection = selection
        self._population = None
        super().__init__(
            island_name,
            restart_cond
        )

    def reset_state(self):
        self._population = None

    @property
    def current_state(self) -> List[Point]:
        return self._population

    def iterate(
            self,
            points: List[Point]
    ) -> List[Searchable]:
        self._population = self.join(self._population, points) \
            if self._population is not None else points
        return self.tweak(self.select(self._population))

    def select(
            self,
            parents: List[Point]
    ) -> List[Searchable]:
        points = self.selection.select(parents, self.tweak_size)
        return [point.searchable for point in points]

    def tweak(
            self,
            selected: List[Searchable]
    ) -> List[Searchable]:
        return list(map(self.mutation.mutate, selected))

    def join(
            self,
            parents: List[Point],
            offspring: List[Point]
    ) -> List[Point]:
        raise NotImplementedError


class MuPlusLambda(Evolution):
    slug = 'evolution:plus'

    def __init__(
            self,
            mu_size: int,
            lambda_size: int,
            mutation: Mutation,
            selection: Selection,
            island_name: str = None,
            restart_cond: Condition = None
    ):
        self.mu_size = mu_size
        self.tweak_size = lambda_size
        self.lambda_size = lambda_size
        super().__init__(
            mutation,
            selection,
            island_name,
            restart_cond
        )

    def join(
            self,
            parents: List[Point],
            offspring: List[Point]
    ) -> List[Point]:
        parents = parents[:self.mu_size]
        return sorted([*parents, *offspring])


class Genetic(Evolution):
    def __init__(
            self,
            mutation: Mutation,
            crossover: Crossover,
            selection: Selection,
            island_name: str = None,
            restart_cond: Condition = None
    ):
        self.crossover = crossover
        super().__init__(
            mutation,
            selection,
            island_name,
            restart_cond
        )

    def join(
            self,
            parents: List[Point],
            offspring: List[Point]
    ) -> List[Point]:
        raise NotImplementedError

    def tweak(
            self,
            selected: List[Searchable]
    ) -> List[Searchable]:
        return list(chain(*(map(
            self.mutation.mutate,
            self.crossover.cross2(ind1, ind2)
        ) for ind1, ind2 in slice_by(selected, 2))))


class Elitism(Genetic):
    slug = 'genetic:elitism'

    def __init__(
            self,
            elites_count: int,
            population_size: int,
            mutation: Mutation,
            crossover: Crossover,
            selection: Selection,
            island_name: str = None,
            restart_cond: Condition = None
    ):
        self.elites_count = elites_count
        self.tweak_size = population_size
        self.population_size = population_size
        super().__init__(
            mutation,
            crossover,
            selection,
            island_name,
            restart_cond
        )

    def join(
            self,
            parents: List[Point],
            offspring: List[Point]
    ) -> List[Point]:
        elites = parents[:self.elites_count]
        return sorted([*elites, *offspring])


__all__ = [
    'Island',
    'Elitism',
    'Algorithm',
    'MuPlusLambda',
    # struct
    'Iteration'
]
