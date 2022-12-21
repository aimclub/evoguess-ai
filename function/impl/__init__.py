from .function_rho import RhoFunction
from .function_gad import GuessAndDetermine
from .function_ibs import InverseBackdoorSets
from .function_ips import InversePolynomialSets

functions = {
    RhoFunction.slug: RhoFunction,
    GuessAndDetermine.slug: GuessAndDetermine,
    InverseBackdoorSets.slug: InverseBackdoorSets,
    InversePolynomialSets.slug: InversePolynomialSets
}

__all__ = [
    'functions',
    # impls
    'RhoFunction',
    'GuessAndDetermine',
    'InverseBackdoorSets',
    'InversePolynomialSets'
]
