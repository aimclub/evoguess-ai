from itertools import chain
from typing import Dict, Any, Iterable

from .var import *
from .var_d import *
from .var_i import *
from .var_s import *

from typings.searchable import Supplements, combine

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


def get_var_deps(_vars: Iterable[Var]) -> Iterable[AnyVar]:
    return set(chain(*(_var.deps for _var in _vars)))


def get_var_dims(_vars: Iterable[AnyVar]) -> Iterable[int]:
    return iter([2 if isinstance(_var, int) else _var.dim for _var in _vars])


def get_var_sups(_vars: Iterable[Var], sub: Iterable[int]) -> Supplements:
    var_map = {_var: value for _var, value in zip(_vars, sub)}
    return combine(*(_var.supplements(var_map) for _var in _vars))


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
    # utils
    'var_from',
    'get_var_deps',
    'get_var_dims',
    'get_var_sups'
]
