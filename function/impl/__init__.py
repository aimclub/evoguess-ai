from .function_gad import GuessAndDetermine
from .function_div import DivFunction
from .function_rho import RhoFunction
from .function_rho_t import RhoTFunction

from .function_ibs import InverseBackdoorSets
from .function_ips import InversePolynomialSets

functions = {
    DivFunction.slug: DivFunction,
    RhoFunction.slug: RhoFunction,
    RhoTFunction.slug: RhoTFunction,
    GuessAndDetermine.slug: GuessAndDetermine,
    InverseBackdoorSets.slug: InverseBackdoorSets,
    InversePolynomialSets.slug: InversePolynomialSets
}

__all__ = [
    'functions',
    # impls
    'DivFunction',
    'RhoFunction',
    'RhoTFunction',
    'GuessAndDetermine',
    'InverseBackdoorSets',
    'InversePolynomialSets'
]
