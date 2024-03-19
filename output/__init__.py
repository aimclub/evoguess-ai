from .abc import Logger, Parser
from .impl import outputs
from utility import load_modules


def OutputBuilder(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(**configuration)
    return outputs.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Logger',
    'Parser',
    # builder
    'OutputBuilder'
]
