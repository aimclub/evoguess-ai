from .elitism import *
from .m_plus_l import *
from .m_comma_l import *
from .log_search import *

algorithms = {
    Elitism.slug: Elitism,
    LogSearch.slug: LogSearch,
    MuPlusLambda.slug: MuPlusLambda,
    MuCommaLambda.slug: MuCommaLambda
}

__all__ = [
    'algorithms',
    # impls
    'Elitism',
    'LogSearch',
    'MuPlusLambda',
    'MuCommaLambda'
]
