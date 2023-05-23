from .cnf import *
from .cnfp import *
from .source import *

encodings = {
    CNF.slug: CNF,
    CNFP.slug: CNFP,
    Source.slug: Source,
}

__all__ = [
    # 'AIG',
    'CNF',
    'CNFP',
    'Source',
    # types
    'Clause',
    'Atmost',
    'Clauses',
    'Atmosts',
    'CNFData',
    'CNFPData',
    'SourceData',
]
