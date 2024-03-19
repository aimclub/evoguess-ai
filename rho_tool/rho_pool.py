from typing import Any, Dict

from space.impl import BackdoorSet
from core.model.point import Point

from lib_satprob.solver import _Solver
from lib_satprob.problem import Problem
from lib_satprob.variables import Range
from lib_satprob.encoding.patch import SatPatch

from concurrent.futures import ProcessPoolExecutor

RhoCache = Dict[str, Point]


class RhoProcessState:
    cache: RhoCache = {}
    patch: SatPatch = None
    solver: _Solver = None
    problem: Problem = None
    space: BackdoorSet = None


_rho_process_state = RhoProcessState()


def _pool_initializer(problem: Problem):
    formula = problem.encoding.get_formula()
    solver = problem.solver.get_instance(formula)
    space = BackdoorSet(Range(length=formula.nv))

    _rho_process_state.problem = problem
    _rho_process_state.solver = solver
    _rho_process_state.space = space


def get_process_state() -> RhoProcessState:
    return _rho_process_state


def update_process_cache(point: Point):
    key = str(point.searchable)
    state = _rho_process_state
    state.cache[key] = point


_rho_process_pool = {}


def init_process_pool(
        problem: Problem,
        max_workers: int
) -> ProcessPoolExecutor:
    return ProcessPoolExecutor(
        initargs=(problem,),
        max_workers=max_workers,
        initializer=_pool_initializer,
    )


__all__ = [
    'init_process_pool',
    'get_process_state',
]
