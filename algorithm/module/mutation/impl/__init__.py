from .doer import *
from .one_bit import *
from .uniform import *
from .log_div import *
from .fix_size import *

mutations = {
    Doer.slug: Doer,
    LogDiv.slug: LogDiv,
    OneBit.slug: OneBit,
    Uniform.slug: Uniform,
    FixSize.slug: FixSize,
}

__all__ = [
    'Doer',
    'LogDiv',
    'OneBit',
    'Uniform',
    'FixSize'
]
