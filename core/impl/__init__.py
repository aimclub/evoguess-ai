from .combine import *
from .optimize import *
from .combine_t import *
from .growing_t import *

cores = {
    Combine.slug: Combine,
    Optimize.slug: Optimize,
    CombineT.slug: CombineT,
    GrowingT.slug: GrowingT
}
