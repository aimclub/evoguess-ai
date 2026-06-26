from typing import Dict, Any, Iterable, Optional, List
from itertools import chain

from utility.iterable import compact, split_by
from .._utility import Supplements, combine

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

def is_index(_var: Var) -> bool:
    return isinstance(_var, Index)

def to_var_str(_vars: Iterable[Var]) -> str:
    index_vars, other_var = split_by(_vars, is_index)
    indexes = compact([v.index for v in index_vars])
    return ' '.join([*map(str, other_var), indexes])

def get_var_deps(_vars: Iterable[Var]) -> Iterable[AnyVar]:
    return set(chain(*(_var.deps for _var in _vars)))


def get_var_dims(_vars: Iterable[AnyVar]) -> Iterable[int]:
    return iter([2 if isinstance(_var, int) else _var.dim for _var in _vars])


def get_var_sups(_vars: Iterable[Var], using_var_map: Optional[VarMap] = None,
                 using_values: Optional[List[int]] = None) -> Supplements:
    var_map = using_var_map if using_values is None else {
        _var: value for _var, value in zip(_vars, using_values)
    }
    return combine(*(_var.substitute(var_map) for _var in _vars))


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
    'to_var_str',
    'get_var_deps',
    'get_var_dims',
    'get_var_sups',
]
