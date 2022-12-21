from .elitism import *
from .m_plus_l import *
from .m_comma_l import *

algorithms = {
    Elitism.slug: Elitism,
    MuPlusLambda.slug: MuPlusLambda,
    MuCommaLambda.slug: MuCommaLambda
}

__all__ = [
    'algorithms',
    # impls
    'Elitism',
    'MuPlusLambda'
]
