from .cnf import *
from .wcnf import *

encodings = {
    CNF.slug: CNF,
    WCNF.slug: WCNF,
    CNFPlus.slug: CNFPlus,
    WCNFPlus.slug: WCNFPlus,
}

__all__ = [
    # 'AIG',
    'CNF',
    'WCNF',
    'CNFPlus',
    'WCNFPlus',
    # types
    'Clause',
    'Clauses'
]
