import sys
import time
from typing import Sized


def time_ms() -> int:
    return time.time_ns() // 1_000_000


STAMP = time_ms()


def sized(x: Sized):
    return len(x), x


def timeh(value: int) -> str:
    hs = f'{value // 3600:03d}:'
    value = value % 3600
    ms = f'{value // 60:02d}:'
    value = value % 60
    ss = f'{value // 1:02d}'
    return f'{hs}{ms}{ss}'


def passed(since: int = STAMP) -> float:
    return (time_ms() - since) / 1_000


def passedh(since: int = STAMP) -> str:
    return timeh(int(passed(since)))


def printc(*lines: str, limit: int = 80):
    for size, line in map(sized, lines):
        if size == 0:
            print(passedh(), end=' ')
            print('-' * (limit + 2))
        else:
            print(passedh(), end=' ')
            lc = rc = max(0, limit - size) // 2
            if (limit - size) % 2 == 1:
                if rc: rc += 1
            print('-' * lc, line, '-' * rc)

    sys.stdout.flush()


__all__ = [
    'timeh',
    'printc',
    'passed',
    'passedh',
    # utils
    'time_ms'
]
