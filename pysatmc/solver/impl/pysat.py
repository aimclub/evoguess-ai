from math import copysign
from optparse import Option
from threading import Timer
from time import time as now
from typing import Dict, Union, \
    Tuple, Optional, NamedTuple, Any

from pysat.examples.rc2 import RC2
from pysat import solvers as slv, formula as fml

from pysatmc.encoding import Formula
from pysatmc._utility import Assumptions, Constraints, Supplements
from pysatmc.solver.solver import Solver, _Solver, Report, KeyLimit, UNLIMITED


#
# ==============================================================================
class PySatSetts(NamedTuple):
    sat_name: str
    max_sat_alg: str


#
# ==============================================================================
class PySatTimer:
    def __init__(self, solver: slv.Solver, limit: KeyLimit):
        self._timer = None
        self._solver = solver
        self._timestamp = None
        self.key, self.limit = limit

    def value(self) -> float:
        return now() - self._timestamp

    def interrupt(self):
        if self._solver:
            self._solver.interrupt()

    def __enter__(self):
        if self.limit is not None:
            if self.key == 'time':
                self._timer = Timer(self.limit, self.interrupt, ())
                self._timer.start()
            elif self.key == 'conflicts':
                self._solver.conf_budget(int(self.limit))
            elif self.key == 'propagations':
                self._solver.prop_budget(int(self.limit))
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


#
# ==============================================================================
class _RC2(RC2):
    status = None

    def get_core(self):
        super().get_core()
        return self.core

    def solve(self, assumptions=()):
        self.status = self._compute(assumptions, False)
        return self.status

    def get_model(self):
        if self.status:
            model = self.oracle.get_model()
            model = [v for v in model if abs(v) in self.vmap.i2e]
            model = [int(copysign(self.vmap.i2e[abs(v)], v)) for v in model]
            return sorted(model, key=lambda l: abs(l))

    def solve_limited(self, assumptions=(), expect_interrupt=False):
        self.status = self._compute(assumptions, expect_interrupt, True)
        return self.status

    def _compute(self, assumptions, expect_interrupt, limited=False):
        if self.adapt:
            self.adapt_am1()

        def _process():
            _assumptions = assumptions + self.sels + self.sums
            return self.oracle.solve(_assumptions) if not limited else \
                self.oracle.solve_limited(_assumptions, expect_interrupt)

        _status = False
        while not _status:
            _status = _process()
            if not self.get_core():
                return _status
            self.process_core()
            print(self.accum_stats())

        return True

    def interrupt(self):
        if self.oracle:
            self.oracle.interrupt()

    def accum_stats(self):
        return self.oracle.accum_stats()

    def conf_budget(self, budget=-1):
        if self.oracle:
            self.oracle.conf_budget(budget)

    def prop_budget(self, budget=-1):
        if self.oracle:
            self.oracle.prop_budget(budget)

    def append_formula(self, constraints=()):
        for clause in constraints:
            self.add_clause(clause)
        return self


#
# ==============================================================================
AnySolver = Union[slv.Solver, _RC2]


#
# ==============================================================================
def _solve(
        solver: slv.Solver, assumptions: Assumptions = (),
        limit: KeyLimit = UNLIMITED, extract_model: bool = False,
        use_timer: bool = True
) -> Report:
    if not use_timer and limit == UNLIMITED:
        status = solver.solve(assumptions)
        stats = solver.accum_stats()
    else:
        with PySatTimer(solver, limit) as timer:
            status = solver.solve_limited(assumptions, True)
            stats = {**solver.accum_stats(), 'time': timer.value()}

    return Report(
        status, stats, solver.get_model() if
        extract_model and status else None
    )


#
# ==============================================================================
def _propagate(
        solver: slv.Solver, assumptions: Assumptions = ()
) -> Report:
    stamp, (status, literals) = now(), solver.propagate(assumptions)
    stats = {**solver.accum_stats(), 'time': now() - stamp}

    # pysat: The status is ``True`` if NO conflict arisen
    # during propagation. Otherwise, the status is ``False``.

    # evoguess: The status is ``True`` if NO conflict arisen
    # during propagation and all literals in formula assigned.
    # The status is ``False`` if conflict arisen.
    # Otherwise, the status is ``None``.

    all_assigned = len(literals) >= solver.nof_vars()
    return Report(status and (all_assigned or None), stats, literals)


#
# ==============================================================================
def get_max_sat_alg(settings: PySatSetts, formula: fml.WCNF):
    if settings.max_sat_alg == 'rc2':
        return _RC2(formula, settings.sat_name)


#
# ==============================================================================
class _PySat(_Solver):
    _solver = None
    _last_stats = {}

    def __init__(
            self, formula: Formula,
            settings: PySatSetts,
            use_timer: bool = True
    ):
        self.settings = settings
        super().__init__(formula, use_timer)

    def __enter__(self) -> '_PySat':
        return self

    def __exit__(self, *args):
        if self._solver:
            self._solver.delete()
            self._solver = None

    def _create(
            self, formula: Formula, supplements: Supplements
    ) -> Tuple[Optional[AnySolver], Assumptions]:
        assumptions, constraints = supplements
        if isinstance(formula, fml.CNF):
            name = self.settings.sat_name
            if len(constraints) > 0:
                solver = slv.Solver(name, formula)
                solver.append_formula(constraints)
                return solver.solver, assumptions
            elif self._solver is None:
                solver = slv.Solver(name, formula)
                self._solver = solver.solver
            return None, assumptions
        elif isinstance(formula, fml.WCNF):
            return get_max_sat_alg(
                self.settings, formula
            ).append_formula(constraints + [
                [lit] for lit in assumptions
            ]), []
        else:
            raise TypeError(f'Unknown formula {type(formula)}')

    def _fix_stats(self, report):
        fixed_stats = {
            key: value if key == 'time' else
            value - self._last_stats.get(key, 0)
            for key, value in report.stats.items()
        }
        status, self.last_stats, model = report
        return Report(status, fixed_stats, model)

    def solve(
            self, supplements: Supplements,
            limit: KeyLimit = UNLIMITED,
            extract_model: bool = False
    ) -> Report:
        solver, assumptions = self._create(self.formula, supplements)
        if solver is None: return self._fix_stats(_solve(
            self._solver, assumptions, limit, extract_model, self.use_timer
        ))
        with solver: return _solve(
            solver, assumptions, limit, extract_model, self.use_timer
        )

    def propagate(self, supplements: Supplements) -> Report:
        solver, assumptions = self._create(self.formula, supplements)
        if solver is None: return self._fix_stats(
            _propagate(self._solver, assumptions)
        )
        with solver: return _propagate(solver, assumptions)


#
# ==============================================================================
class PySat(Solver):
    slug = 'solver:pysat'

    def __init__(self, sat_name: str = 'm22', max_sat_alg: str = 'rc2'):
        self.settings = PySatSetts(sat_name, max_sat_alg)

    def use_incremental(
            self, formula: Formula, use_timer: bool = True
    ) -> _PySat:
        return _PySat(formula, self.settings, use_timer)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug
        }


__all__ = [
    'PySat',
    '_PySat',
    # types
    'PySatSetts',
    'PySatTimer',
]
