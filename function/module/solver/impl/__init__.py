from . import pysat
from .pysat import *
from .two_sat import *
from .external import *

solvers = {
    TwoSAT.slug: TwoSAT,
    Kissat.slug: Kissat,
    Cadical.slug: Cadical,
    Glucose3.slug: Glucose3,
    Glucose4.slug: Glucose4,
    Lingeling.slug: Lingeling,
    MapleCM.slug: MapleCM,
    MapleSAT.slug: MapleSAT,
    MapleChrono.slug: MapleChrono,
    Minicard.slug: Minicard,
    Minisat22.slug: Minisat22,
    MinisatGH.slug: MinisatGH,
}

__all__ = [
    'pysat',
    'TwoSAT',
    'Kissat'
]
