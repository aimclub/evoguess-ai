from .pysat import *

solvers = {
    PySatSolver.slug: PySatSolver,
}

__all__ = [
    'PySatSolver',
    '_PySatSolver',
    # types
    'PySatSetts',
    'PySatTimer',
]
