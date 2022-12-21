from .abc import Core
from .impl import cores
from .module import modules

from util import load_modules


def CoreBuilder(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(modules, **configuration)
    return cores.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Core',
    # builder
    'CoreBuilder',
]
