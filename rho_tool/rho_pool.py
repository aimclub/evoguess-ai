from typing import Dict, List
from pysat.solvers import Solver

from space.model import Backdoor
from space.impl import BackdoorSet
from core.model.point import Point

from lib_satprob.problem import Problem
from lib_satprob.encoding import PySatFormula
from lib_satprob.encoding.patch import SatPatch
from lib_satprob.solver import _Solver, PySatSolver

from lib_satprob.variables import Range, Clauses, prod
from lib_satprob.variables.vars import Var

from concurrent.futures import ProcessPoolExecutor

RhoCache = Dict[str, Point]


def _map_clauses(clauses):
    for clause in clauses:
        if not clause: continue
        yield clause, tuple(clause)


class RhoProcessState:
    _constraints = set()
    _var_weights = None
    _sub_solver = None
    _patches = set()
    _formula = None
    _solver = None

    cache: RhoCache = {}
    problem: Problem = None
    space: BackdoorSet = None

    def rm_literals(self, literals: List[int]):
        def not_in(var: Var) -> bool:
            return str(var) not in _vars

        _nums = map(abs, literals)
        _vars = list(map(str, _nums))
        self.space.variables = list(filter(
            not_in, self.space.variables
        ))
        # if self._var_weights:
        #     for var_key in _vars:
        #         del self._var_weights[
        #             var_key
        #         ]

    def add_clauses(self, clauses: Clauses):
        for cl, scl in _map_clauses(clauses):
            if scl in self._constraints:
                continue

            self._constraints.add(scl)
            if self._formula is not None:
                self._formula.append(cl)

            if self._solver is not None:
                self._solver.add_clause(cl, False)
            if self._sub_solver is not None:
                self._sub_solver.add_clause(cl, False)

    def apply_patch(self, patch: SatPatch):
        if patch.filename not in self._patches:
            self._patches.add(patch.filename)
            self.add_clauses(patch.clauses)

    @property
    def formula(self) -> PySatFormula:
        if self._formula is None:
            _enc = self.problem.encoding
            self._formula = _enc.get_formula(False)
            _clauses = map(list, self._constraints)
            self._formula.extend(list(_clauses))

        return self._formula

    @property
    def solver(self) -> _Solver:
        if self._solver is None:
            slv = self.problem.solver
            self._solver = slv.get_instance(
                self.formula, use_timer=False
            )

        return self._solver

    @property
    def sub_solver(self) -> _Solver:
        if self._sub_solver is None:
            slv = PySatSolver(sat_name='m22')
            self._sub_solver = slv.get_instance(
                self.formula, use_timer=False
            )

        return self._sub_solver

    def get_initial(self, size: int, rs_state) -> Backdoor:
        if self._var_weights is None:
            with Solver('m22', self.formula) as slv:
                self._var_weights = {index: prod([
                    len(slv.propagate(var.sub(1))[1]),
                    len(slv.propagate(var.sub(0))[1])
                ]) for index, var in enumerate(
                    self.space.variables
                )}

        best_indexes = [x[0] for x in sorted(
            self._var_weights.items(),
            key=lambda x: -x[1]
        )[:200]]

        indexes = set(rs_state.choice(
            best_indexes, size
        ))
        vector = [
            1 if i in indexes else 0 for
            i in range(len(self._var_weights))
        ]
        return self.space.get_by(vector)


_rho_process_state = RhoProcessState()


def _pool_initializer(problem: Problem):
    formula = problem.encoding.get_formula()
    space = BackdoorSet(Range(length=formula.nv))

    _rho_process_state.problem = problem
    _rho_process_state.space = space


def get_process_state() -> RhoProcessState:
    return _rho_process_state


def init_process_pool(
        problem: Problem,
        max_workers: int
) -> ProcessPoolExecutor:
    return ProcessPoolExecutor(
        initargs=(problem,),
        max_workers=max_workers,
        initializer=_pool_initializer,
    )


__all__ = [
    'init_process_pool',
    'get_process_state',
]
