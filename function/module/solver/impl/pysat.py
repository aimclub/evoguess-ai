from typing import Type
from threading import Timer
from time import time as now
from pysat import solvers as pysat

from ..solver import Report, Solver, IncrSolver

from function.module.budget import KeyLimit, UNLIMITED
from instance.module.encoding import EncodingData, CNFData, CNFPData
from typings.searchable import Assumptions, Constraints, Supplements


class PySatTimer:
    def __init__(self, solver: pysat.Solver, limit: KeyLimit):
        self._timer = None
        self._solver = solver
        self._timestamp = None
        self.key, self.value = limit

    def get_time(self) -> float:
        return now() - self._timestamp

    def interrupt(self):
        if self._solver:
            self._solver.interrupt()

    def __enter__(self):
        if self.value is not None:
            if self.key == 'time':
                self._timer = Timer(self.value, self.interrupt, ())
                self._timer.start()
            elif self.key == 'conflicts':
                self._solver.conf_budget(int(self.value))
            elif self.key == 'propagations':
                self._solver.prop_budget(int(self.value))
            else:
                raise KeyError(f'PySat don\'t support {self.key} limit')

        self._timestamp = now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._timer is not None:
            if self._timer.is_alive():
                self._timer.cancel()
            self._timer = None
        self._solver = None


def init(constructor: Type, encoding_data: EncodingData,
         constraints: Constraints) -> pysat.Solver:
    if isinstance(encoding_data, CNFData):
        clauses = encoding_data.clauses(constraints)
        solver = constructor(clauses, True)
        if isinstance(encoding_data, CNFPData):
            for literals, rhs in encoding_data.atmosts():
                solver.add_atmost(literals, rhs)
    else:
        raise TypeError('PySat works only with CNF or CNF+ encodings')
    return solver


def solve(solver: pysat.Solver, assumptions: Assumptions = (),
          limit: KeyLimit = UNLIMITED, add_model: bool = False) -> Report:
    with PySatTimer(solver, limit) as timer:
        status = solver.solve_limited(assumptions, expect_interrupt=True)
        stats = {**solver.accum_stats(), 'time': timer.get_time()}

    model = None
    if add_model and status:
        model = solver.get_model()
    return Report(status, stats, model)


def propagate(solver: pysat.Solver, assumptions: Assumptions = ()) -> Report:
    with PySatTimer(solver, UNLIMITED) as timer:
        status, literals = solver.propagate(assumptions)
        stats = {**solver.accum_stats(), 'time': timer.get_time()}

    # pysat: The status is ``True`` if NO conflict arisen
    # during propagation. Otherwise, the status is ``False``.

    # evoguess: The status is ``True`` if conflict arisen
    # during propagation or all literals in formula assigned.
    # Otherwise, the status is ``False``.

    max_literal = solver.nof_vars()
    status = not (status and len(literals) < max_literal)
    return Report(status, stats, literals)


class IncrPySAT(IncrSolver):
    solver = None
    last_stats = {}

    def __init__(self, encoding_data: EncodingData,
                 constraints: Constraints, constructor: Type):
        super().__init__(encoding_data, constraints)
        self.constructor = constructor

    def _fix(self, report: Report) -> Report:
        fixed_stats = {
            key: value if key == 'time' else
            value - self.last_stats.get(key, 0)
            for key, value in report.stats.items()
        }
        status, self.last_stats, model = report
        return Report(status, fixed_stats, model)

    def __enter__(self):
        self.solver = init(
            self.constructor,
            self.encoding_data,
            self.constraints,
        )
        self.last_fixed_value = 0
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.solver:
            self.solver.delete()
            self.solver = None

    def solve(self, assumptions: Assumptions,
              limit: KeyLimit = UNLIMITED,
              add_model: bool = False) -> Report:
        return self._fix(solve(self.solver, assumptions, limit, add_model))

    def propagate(self, assumptions: Assumptions) -> Report:
        return self._fix(propagate(self.solver, assumptions))


class PySAT(Solver):
    def __init__(self, constructor: Type):
        self.constructor = constructor

    def use_incremental(self, encoding_data: EncodingData,
                        constraints: Constraints = ()) -> IncrPySAT:
        return IncrPySAT(encoding_data, constraints, self.constructor)

    def solve(self, encoding_data: EncodingData, supplements: Supplements,
              limit: KeyLimit = UNLIMITED, add_model: bool = False) -> Report:
        assumptions, constraints = supplements
        with init(self.constructor, encoding_data, constraints) as solver:
            return solve(solver, assumptions, limit, add_model)

    def propagate(self, encoding_data: EncodingData, supplements: Supplements) -> Report:
        assumptions, constraints = supplements
        with init(self.constructor, encoding_data, constraints) as solver:
            return propagate(solver, assumptions)


class Cadical(PySAT):
    slug = 'solver:pysat:cd'

    def __init__(self):
        super().__init__(pysat.Cadical)


class Glucose3(PySAT):
    slug = 'solver:pysat:g3'

    def __init__(self):
        super().__init__(pysat.Glucose3)


class Glucose4(PySAT):
    slug = 'solver:pysat:g4'

    def __init__(self):
        super().__init__(pysat.Glucose4)


class Lingeling(PySAT):
    slug = 'solver:pysat:lgl'

    def __init__(self):
        super().__init__(pysat.Lingeling)


class MapleCM(PySAT):
    slug = 'solver:pysat:mcm'

    def __init__(self):
        super().__init__(pysat.MapleCM)


class MapleSAT(PySAT):
    slug = 'solver:pysat:mpl'

    def __init__(self):
        super().__init__(pysat.Maplesat)


class MapleChrono(PySAT):
    slug = 'solver:pysat:mcb'

    def __init__(self):
        super().__init__(pysat.MapleChrono)


class Minicard(PySAT):
    slug = 'solver:pysat:mc'

    def __init__(self):
        super().__init__(pysat.Minicard)


class Minisat22(PySAT):
    slug = 'solver:pysat:mgh'

    def __init__(self):
        super().__init__(pysat.Minisat22)


class MinisatGH(PySAT):
    slug = 'solver:pysat:m22'

    def __init__(self):
        super().__init__(pysat.MinisatGH)


__all__ = [
    'Cadical',
    'Glucose3',
    'Glucose4',
    'Lingeling',
    'MapleCM',
    'MapleSAT',
    'MapleChrono',
    'Minicard',
    'Minisat22',
    'MinisatGH',
    # types
    'PySAT',
    'IncrPySAT'
]
