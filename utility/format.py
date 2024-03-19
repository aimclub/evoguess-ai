import sys
import time
from typing import Sized


def time_ms() -> int:
    return time.time_ns() // 1_000_000


STAMP = time_ms()


def sized(x: Sized):
    return len(x), x


def timeh(value: int) -> str:
    s = ''
    for period in [3600, 60]:
        part = value // period
        s += f'{part:02d}:'
        value %= period
    return f'{s}{value:02d}'


def passed(since: int = STAMP) -> float:
    return (time_ms() - since) / 1_000


def passedh(since: int = STAMP) -> str:
    return timeh(int(passed(since)))


def printc(*lines: str, limit: int = 65):
    for size, line in map(sized, lines):
        if size == 0:
            print(passedh(), end=' ')
            print('-' * (limit + 2))
        else:
            print(passedh(), end=' ')
            cnt = max(0, limit - size) // 2
            print('-' * cnt, line, '-' * cnt)

    sys.stdout.flush()


__all__ = [
    'timeh',
    'printc',
    'passed',
    'passedh',
    # utils
    'time_ms'
]
