from .abc import Space
from .impl import spaces


def SpaceBuilder(configuration, **kwargs):
    slug = configuration.pop('slug')
    return spaces.get(slug)(**kwargs)


__all__ = [
    'Space',
    # builder
    'SpaceBuilder'
]
