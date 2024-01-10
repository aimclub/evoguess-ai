from .backdoor_set import *
from .interval_set import *
from .partition_set import *

spaces = {
    BackdoorSet.slug: BackdoorSet,
    IntervalSet.slug: IntervalSet,
    PartitionSet.slug: PartitionSet
}

__all__ = [
    'spaces',
    # impls
    'BackdoorSet',
    'IntervalSet',
    'PartitionSet',
]
