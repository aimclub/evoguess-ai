from .abc import Algorithm
from .impl import algorithms
from .module import modules

from utility import load_modules


def AlgorithmBuilder(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(modules, **configuration)
    return algorithms.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Algorithm',
    # builder
    'AlgorithmBuilder'
]
