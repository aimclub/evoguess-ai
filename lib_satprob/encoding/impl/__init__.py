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
    # utility
    'wcnf_to_cnf'
]
