from .walltime import *
from .iteration import *

limitations = {
    WallTime.slug: WallTime,
    Iteration.slug: Iteration,
}

__all__ = [
    'WallTime',
    'Iteration',
]
