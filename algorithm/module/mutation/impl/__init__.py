from .doer import *
from .one_bit import *
from .uniform import *

mutations = {
    Doer.slug: Doer,
    OneBit.slug: OneBit,
    Uniform.slug: Uniform,
}

__all__ = [
    'Doer',
    'OneBit',
    'Uniform'
]
