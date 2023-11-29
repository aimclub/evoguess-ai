from .abc import Space
from .impl import spaces

from ._utility import *


def SpaceBuilder(configuration, **kwargs):
    slug = configuration.pop('slug')
    return spaces.get(slug)(**kwargs)


__all__ = [
    'Space',
    # utility
    'rho_subset',
    # builder
    'SpaceBuilder'
]
