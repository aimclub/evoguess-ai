from typing import List

from lib_satprob.variables import Clauses, Supplements

try:
    from pyeda.boolalg.expr import AndOp, Variable
    from pyeda.inter import Or, And, exprvar, espresso_exprs
except ModuleNotFoundError:
    pass


def to_dnf_var(lit: int) -> 'Variable':
    var = exprvar('x', abs(lit))
    return var if lit > 0 else ~var


def to_dnf_clause(cube: Supplements) -> 'AndOp':
    return And(*map(to_dnf_var, cube[0]))


def _get_derived_by(easy: List[Supplements]) -> Clauses:
    dnf = Or(*map(to_dnf_clause, easy))
    (min_dnf,) = espresso_exprs(dnf)
    min_cnf = (~min_dnf).to_cnf()

    lit_map, _, cnf = min_cnf.encode_cnf()

    def map_lit(lit: int) -> int:
        var = lit_map[abs(lit)].indices[0]
        return var if lit > 0 else -var

    # noinspection PyTypeChecker
    return [sorted(map(map_lit, cl), key=abs) for cl in cnf]


def get_derived_by(easy: List[Supplements]) -> Supplements:
    one_lit, constraints = [], []
    for clause in _get_derived_by(easy):
        (one_lit if len(clause) == 1
         else constraints).append(clause)

    return [cl[0] for cl in one_lit], constraints


__all__ = [
    'get_derived_by',
    '_get_derived_by'
]
