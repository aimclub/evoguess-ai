from typing import List, Tuple

Clause = List[int]
Clauses = List[Clause]

Assumptions = List[int]
Constraints = Clauses
Supplements = Tuple[
    Assumptions,
    Constraints
]


def combine(*args: Supplements) -> Supplements:
    # todo: check repeated and delete it
    assumptions, constraints = [], []
    for supplements in args:
        assumptions.extend(supplements[0])
        constraints.extend(supplements[1])
    return assumptions, constraints


try:  # for python3.8 and greater
    from math import prod
except ImportError:  # for python3.7
    from operator import mul
    from functools import reduce


    def prod(_list):
        return reduce(mul, _list, 1)

__all__ = [
    'Clause',
    'Clauses',
    'Assumptions',
    'Constraints',
    'Supplements',
    # utils
    'prod',
    'combine',
]
