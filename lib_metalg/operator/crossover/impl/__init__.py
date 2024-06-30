from .uniform import *
from .one_point import *
from .two_point import *
from .same_size import *

crossovers = {
    Uniform.slug: Uniform,
    SameSize.slug: SameSize,
    OnePoint.slug: OnePoint,
    TwoPoint.slug: TwoPoint,
}

__all__ = [
    'Uniform',
    'SameSize',
    'OnePoint',
    'TwoPoint'
]
