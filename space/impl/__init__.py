from .backdoor_set import *
from .interval_set import *

spaces = {
    BackdoorSet.slug: BackdoorSet,
    IntervalSet.slug: IntervalSet,
}

__all__ = [
    'spaces',
    # impls
    'BackdoorSet',
    'IntervalSet',
]
