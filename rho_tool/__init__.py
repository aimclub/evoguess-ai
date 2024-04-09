from typing import List

from .rho_func import *
from .rho_pool import *
from .rho_order import *

from space.model import Backdoor
from core.model.point import Point
from core.module.comparator import MinValueMaxSize

COMPARATOR = MinValueMaxSize()


def hard_to_num(hard_task: List[int]) -> int:
    return sum([
        2 ** i if lit > 0 else 0 for i, lit in
        enumerate(sorted(hard_task, key=abs)[::-1])
    ])


def _rho_fn(backdoor: Backdoor) -> RhoStats:
    variables = backdoor.variables()
    solver = get_process_state().solver
    return _rho_func_tree(solver, variables)


def rho_fn(backdoor: Backdoor) -> Point:
    _, _, rho_value, tasks = _rho_fn(backdoor)
    return Point(backdoor, COMPARATOR).set(
        hard=len(tasks), value=1 - rho_value,
        first_task=len(tasks) and tasks[0]
    )


def rho_fn_ext(backdoor: Backdoor) -> Point:
    _, _, rho_value, tasks = _rho_fn(backdoor)
    return Point(backdoor, COMPARATOR).set(
        hard=len(tasks), value=1 - rho_value,
        hard_nums=list(map(hard_to_num, tasks))
    )


__all__ = [
    'rho_fn',
    'rho_fn_ext'
]
