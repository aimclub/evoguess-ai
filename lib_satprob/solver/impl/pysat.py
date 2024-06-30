from math import copysign
from threading import Timer
from time import time as now
from typing import Dict, Union, \
    Any, Tuple, Optional, NamedTuple

from pysat import solvers as slv
from pysat.examples.rc2 import RC2

from ..solver import Report, Solver, \
    _Solver, KeyLimit, UNLIMITED

from ...encoding import PySatFormula, MaxSatFormula, \
    to_sat_formula, is_sat_formula, is_max_sat_formula
from ...variables import Assumptions, Supplements, Clause


#
# ==============================================================================
class PySatSetts(NamedTuple):
    sat_name: str
    max_sat_alg: str


# def is_supports_atms(sat_name: str) -> bool:
#     return sat_name in slv.SolverNames.gluecard3 or \
#            sat_name in slv.SolverNames.gluecard4 or \
#            sat_name in slv.SolverNames.minicard


#
# ==============================================================================
class FormulaError(TypeError):
    def __init__(self, formula: PySatFormula):
        super().__init__(f'Unknown formula {type(formula)}')


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
            self._solver.clear_interrupt()

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
        assert not assumptions, 'Not empty assumptions'
        self.status = self._compute(False)
        return self.status

    def get_model(self):
        if self.status:
            model = self.oracle.get_model()
            model = [v for v in model if abs(v) in self.vmap.i2e]
            model = [int(copysign(self.vmap.i2e[abs(v)], v)) for v in model]
            return sorted(model, key=lambda l: abs(l))

    def solve_limited(self, assumptions=(), expect_interrupt=False):
        assert not assumptions, 'Not empty assumptions'
        self.status = self._compute(expect_interrupt, True)
        return self.status

    def _compute(self, expect_interrupt, limited=False):
        if self.adapt:
            self.adapt_am1()

        _status = False
        while not _status:
            _status = self.oracle.solve_limited(
                self.sels + self.sums,
                expect_interrupt
            ) if limited else self.oracle.solve(
                self.sels + self.sums
            )

            if not self.get_core():
                return _status
            self.process_core()

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
def _solve(solver: AnySolver, assumptions: Assumptions, limit: KeyLimit,
           extract_model: bool, use_timer: bool) -> Report:
    if not use_timer and limit == UNLIMITED:
        status = solver.solve(assumptions)
        stats = solver.accum_stats()
    else:
        with PySatTimer(solver, limit) as timer:
            status = solver.solve_limited(assumptions, True)
            stats = {**solver.accum_stats(), 'time': timer.value()}

    cost = solver.cost if status and isinstance(solver, _RC2) else None
    model = solver.get_model() if extract_model and status else None
    return Report(status, stats, model, cost)


#
# ==============================================================================
def _propagate(solver: AnySolver, assumptions: Assumptions) -> Report:
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
def get_max_sat_alg(settings: PySatSetts, formula: MaxSatFormula):
    if settings.max_sat_alg == 'rc2':
        return _RC2(formula, settings.sat_name)


#
# ==============================================================================
class _PySatSolver(_Solver):
    _solver = None
    _last_stats = {}

    def __init__(
            self,
            formula: PySatFormula,
            settings: PySatSetts,
            use_timer: bool = True
    ):
        self.settings = settings
        super().__init__(formula, use_timer)

    def __enter__(self) -> '_PySatSolver':
        return self

    def __exit__(self, *args):
        if self._solver:
            self._solver.delete()
            self._solver = None

    def _init_solver(
            self, supplements: Supplements,
            formula: Optional[PySatFormula] = None
    ) -> Tuple[Optional[AnySolver], Assumptions]:
        name = self.settings.sat_name
        formula = formula or self.formula
        assumptions, constraints = supplements

        if is_sat_formula(formula):
            if len(constraints) > 0:
                solver = slv.Solver(name, formula)
                solver.append_formula(constraints)
                return solver, assumptions
            elif self._solver is None:
                solver = slv.Solver(name, formula)
                self._solver = solver.solver
                solver.solver = None
            return None, assumptions
        elif is_max_sat_formula(formula):
            return get_max_sat_alg(
                self.settings, formula
            ).append_formula(constraints + [
                [lit] for lit in assumptions
            ]), []
        else:
            raise FormulaError(formula)

    def _fix_stats(self, report: Report) -> Report:
        fixed_stats = {
            key: value if key == 'time' else
            value - self._last_stats.get(key, 0)
            for key, value in report.stats.items()
        }
        status, self._last_stats, model, weight = report
        return Report(status, fixed_stats, model, weight)

    def solve(
            self, supplements: Supplements,
            limit: KeyLimit = UNLIMITED,
            extract_model: bool = True,
    ) -> Report:
        assumptions, constraints = supplements
        args = (limit, extract_model, self.use_timer)

        solver, assumptions = self._init_solver(
            (assumptions, constraints), self.formula
        )
        if not solver: return self._fix_stats(
            _solve(self._solver, assumptions, *args)
        )
        with solver:
            return _solve(solver, assumptions, *args)

    def propagate(
            self, supplements: Supplements,
            ignore_constraints: bool = False
    ) -> Report:
        assumptions, constraints = supplements
        if ignore_constraints: constraints = []

        # todo: make to_sat_formula lazy
        formula = to_sat_formula(self.formula)
        solver, assumptions = self._init_solver(
            (assumptions, constraints), formula
        )
        if not solver: return self._fix_stats(
            _propagate(self._solver, assumptions)
        )
        with solver:
            return _propagate(solver, assumptions)

    def add_clause(
            self, clause: Clause,
            append_to_formula: bool = True
    ) -> '_PySatSolver':
        if append_to_formula:
            self.formula.append(clause)
        if self._solver is not None:
            self._solver.add_clause(clause)
        return self


#
# ==============================================================================
class PySatSolver(Solver):
    slug = 'solver:pysat'

    def __init__(self, sat_name: str = 'm22', max_sat_alg: str = 'rc2'):
        self.settings = PySatSetts(sat_name, max_sat_alg)

    def get_instance(
            self, formula: PySatFormula, use_timer: bool = True
    ) -> _PySatSolver:
        return _PySatSolver(formula, self.settings, use_timer)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'sat_name': self.settings.sat_name,
            'max_sat_alg': self.settings.max_sat_alg,
        }


__all__ = [
    'PySatSolver',
    '_PySatSolver',
    # types
    'PySatTimer',
    'PySatSetts',
    # errors
    'FormulaError'
]
