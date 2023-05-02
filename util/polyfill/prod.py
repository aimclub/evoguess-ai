try:  # for python3.8 and greater
    from math import prod
except ImportError:  # for python3.7
    from operator import mul
    from functools import reduce


    def prod(_list):
        return reduce(mul, _list, 1)

__all__ = [
    'prod'
]
