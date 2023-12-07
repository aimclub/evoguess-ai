from .combine import *
from .solving import *
from .optimize import *
from .combine_t import *
from .growing_t import *

cores = {
    Solving.slug: Solving,
    Combine.slug: Combine,
    Optimize.slug: Optimize,
    CombineT.slug: CombineT,
    GrowingT.slug: GrowingT
}
