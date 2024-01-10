from .pysat import *
from .py2sat import *
from .external import *

solvers = {
    Kissat.slug: Kissat,
    Loandra.slug: Loandra,
    PySatSolver.slug: PySatSolver,
    Py2SatSolver.slug: Py2SatSolver,
}

__all__ = [
    'Kissat',
    'Loandra',
    'PySatSolver',
    'Py2SatSolver',
    '_PySatSolver',
    '_Py2SatSolver',
    # types
    'PySatSetts',
    'PySatTimer',
]
