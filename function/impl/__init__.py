from .function_gad import GuessAndDetermine
from .function_ibs import InverseBackdoorSets

from .function_rho import RhoFunction
from .function_rho_t import RhoTFunction
from .function_ips import InversePolynomialSets

functions = {
    RhoFunction.slug: RhoFunction,
    RhoTFunction.slug: RhoTFunction,
    GuessAndDetermine.slug: GuessAndDetermine,
    InverseBackdoorSets.slug: InverseBackdoorSets,
    InversePolynomialSets.slug: InversePolynomialSets
}

__all__ = [
    'functions',
    # impls
    'RhoFunction',
    'RhoTFunction',
    'GuessAndDetermine',
    'InverseBackdoorSets',
    'InversePolynomialSets'
]
