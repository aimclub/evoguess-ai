from typing import List, Tuple

Assumptions = List[int]
Constraints = List[List[int]]
Supplements = Tuple[Assumptions, Constraints]


def to_bin(value: int, size: int) -> List[int]:
    return [
        1 if value & (1 << (size - 1 - i))
        else 0 for i in range(size)
    ]


def combine(*args: Supplements) -> Supplements:
    assumptions, constraints = [], []
    for supplements in args:
        assumptions.extend(supplements[0])
        constraints.extend(supplements[1])
    return assumptions, constraints


__all__ = [
    'Assumptions',
    'Constraints',
    'Supplements',
    # utils
    'to_bin',
    'combine',
]
