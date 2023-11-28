from typing import Any, Dict, TypeVar

from .impl import *
from ._utility import *
from . import impl, _utility

from .vars import var_from
from ._enum import Enumerable
from .variables import Variables

impls = {
    **impl.variables,
    Variables.slug: Variables,
}

TVariables = TypeVar('TVariables', bound='Variables')


def variables_from(config: Dict[str, Any]) -> TVariables:
    slug = config.pop('slug')
    if config.get('from_vars') is not None:
        config['from_vars'] = list(map(
            var_from, config['from_vars']
        ))
    return impls[slug](**config)


__all__ = [
    'Variables',
    'Enumerable',
    *impl.__all__,
    *_utility.__all__,
    # from loader
    'variables_from',
]
