from .uniform import *
from .one_point import *
from .two_point import *

crossovers = {
    Uniform.slug: Uniform,
    OnePoint.slug: OnePoint,
    TwoPoint.slug: TwoPoint
}

__all__ = [
    'Uniform',
    'OnePoint',
    'TwoPoint'
]
