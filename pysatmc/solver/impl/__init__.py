from .pysat import *

solvers = {
    PySat.slug: PySat,
}

__all__ = [
    'PySat',
    '_PySat',
    # types
    'PySatSetts',
    'PySatTimer',
]
