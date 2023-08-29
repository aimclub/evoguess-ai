from pysat import formula as fml
from pysat.examples.rc2 import RC2

from .pysat import PySatTimer
from ..solver import Report, Solver, IncrSolver

from instance.module.encoding import Formula
from function.module.budget import KeyLimit, UNLIMITED
from typings.searchable import Constraints, Supplements


class RC2L(RC2):
    def __init__(self, formula: fml.WCNF, limit: KeyLimit):
        self.status, self.limit = None, limit
        super().__init__(formula)

    def compute_(self):
        if self.adapt:
            self.adapt_am1()

        # todo: check limitation is correct
        with PySatTimer(self.oracle, self.limit) as timer:
            while not self.oracle.solve_limited(
                    assumptions=self.sels + self.sums,
                    expect_interrupt=True
            ):
                self.get_core()

                if not self.core:
                    self.status = False
                    return False

                self.process_core()

        self.status = True
        return True


class PyMaxSAT(Solver):
    def __init__(self, solver_name: str):
        self.name = solver_name

    def use_incremental(self, formula: Formula,
                        constraints: Constraints = ()) -> IncrSolver:
        raise RuntimeError('PyMaxSAT solver supports only solve procedure')

    def solve(self, formula: Formula, supplements: Supplements,
              limit: KeyLimit = UNLIMITED, add_model: bool = False) -> Report:
        if isinstance(formula, fml.WCNF):
            solver = RC2L(formula, limit)
            model, status = solver.compute(), solver.status
            return Report(status, solver.oracle.accum_stats(), model)
        else:
            raise TypeError('PyMaxSAT works only with WCNF encodings')

    def propagate(self, formula: Formula, supplements: Supplements) -> Report:
        raise RuntimeError('PyMaxSAT solver supports only solve procedure')


__all__ = [
    'PyMaxSAT'
]
