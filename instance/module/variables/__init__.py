from typing import Any, Dict

from . import impl
from .impl import *
from .variables import *
from .vars import var_from

impls = {
    **impl.variables,
    Variables.slug: Variables,
}


# noinspection PyProtectedMember
def make_backdoor(_variables: Variables) -> Backdoor:
    return Backdoor(
        from_vars=_variables._vars,
        from_file=_variables.filepath,
    )


def variables_from(config: Dict[str, Any]) -> Variables:
    slug = config.pop('slug')
    if config.get('from_vars') is not None:
        config['from_vars'] = list(map(var_from, config['from_vars']))
    return impls[slug](**config)


__all__ = [
    'Variables',
    *impl.__all__,
    # utils
    'make_backdoor',
    'variables_from'
]
