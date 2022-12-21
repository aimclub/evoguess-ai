# from .aig import *
from .cnf import *
from .cnfp import *

encodings = {
    # AIG.slug: AIG,
    CNF.slug: CNF,
    CNFP.slug: CNFP,
}

__all__ = [
    # 'AIG',
    'CNF',
    'CNFP',
    # types
    'Clause',
    'Atmost',
    'Clauses',
    'Atmosts',
    'CNFData',
    'CNFPData',
]
