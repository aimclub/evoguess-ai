from .abc import Executor
from .impl import executors


def ExecutorBuilder(configuration, **kwargs):
    slug = configuration.pop('slug')
    return executors.get(slug)(**kwargs)


__all__ = [
    'Executor',
    # builder
    'ExecutorBuilder'
]
