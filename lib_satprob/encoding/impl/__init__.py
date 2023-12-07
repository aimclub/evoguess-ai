from .pysat import *

encodings = {
    CNF.slug: CNF,
    WCNF.slug: WCNF,
    CNFPlus.slug: CNFPlus,
    WCNFPlus.slug: WCNFPlus,
}

__all__ = [
    'CNF',
    'WCNF',
    'CNFPlus',
    'WCNFPlus',
    # types
    'Clause',
    'Clauses',
    'SatFormula',
    'PySatFormula',
    'MaxSatFormula',
    # utility
    'to_sat_formula',
    'is_sat_formula',
    'is_max_sat_formula'
]
