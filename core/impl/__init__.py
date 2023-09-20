from .combine import *
from .optimize import *
from .combine_t import *

cores = {
    Combine.slug: Combine,
    Optimize.slug: Optimize,
    CombineT.slug: CombineT,
}
