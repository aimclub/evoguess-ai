from typing import List

from lib_satprob.variables import Supplements

try:
    from pyeda.boolalg.expr import AndOp, Variable
    from pyeda.inter import Or, And, exprvar, espresso_exprs
except ModuleNotFoundError:
    pass


def to_dnf_var(lit: int) -> Variable:
    var = exprvar('x', abs(lit))
    return var if lit > 0 else ~var


def to_dnf_clause(cube: Supplements) -> AndOp:
    return And(*map(to_dnf_var, cube[0]))


def get_derived_by(easy: List[Supplements]) -> Supplements:
    dnf = Or(*map(to_dnf_clause, easy))
    (min_dnf,) = espresso_exprs(dnf)
    min_cnf = (~min_dnf).to_cnf()

    one_lit, constraints = [], []
    lit_map, _, cnf = min_cnf.encode_cnf()

    def map_lit(lit: int) -> int:
        var = lit_map[abs(lit)].indices[0]
        return var if lit > 0 else -var

    clauses = [map(map_lit, cl) for cl in cnf]
    for clause in map(lambda x: sorted(x, key=abs), clauses):
        (one_lit if len(clause) == 1 else constraints).append(clause)

    return [clause[0] for clause in one_lit], constraints


__all__ = [
    'get_derived_by'
]
