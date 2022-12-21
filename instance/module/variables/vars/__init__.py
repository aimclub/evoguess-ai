from typing import Dict, Any

from .var import *
from .var_d import *
from .var_i import *
from .var_s import *

var_slugs = {
    Index.slug: Index,
    Domain.slug: Domain,
    XorSwitch.slug: XorSwitch,
    Bent4Switch.slug: Bent4Switch,
    MajoritySwitch.slug: MajoritySwitch,
}


def var_from(config: Dict[str, Any]) -> Var:
    slug = config.pop('slug')
    return var_slugs[slug](**config)


def compress(*args: Supplements) -> Supplements:
    assumptions, constraints = [], []
    for supplements in args:
        assumptions.extend(supplements[0])
        constraints.extend(supplements[1])
    return assumptions, constraints


__all__ = [
    'Index',
    'Domain',
    'Switch',
    'XorSwitch',
    'Bent4Switch',
    'MajoritySwitch',
    # types
    'Var',
    'AnyVar',
    'VarMap',
    'Assumptions',
    'Constraints',
    'Supplements',
    # utils
    'compress',
    'var_from',
]
