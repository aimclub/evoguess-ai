from operator import getitem
from functools import reduce

from . import polyfill, iterable, work_path, wrappers


def _key(function):
    return str(function).split()[1].lower()


def load_modules(modules=(()), **kwargs):
    modules, loaded_kwargs = dict(modules), {}
    for key, value in kwargs.items():
        if isinstance(value, dict):
            slug = value.pop('slug')
            # print(f'load: {key} with {value}')
            value = modules[slug](**load_modules(modules, **value))
        if isinstance(value, str) and '@' in value:
            references = value[1:].split('.')
            value = reduce(getitem, references, loaded_kwargs)
        loaded_kwargs[key] = value
    return loaded_kwargs


def build(structure, **kwargs):
    constructor, deps = list(structure.items())[0]
    key = _key(constructor)
    return key, constructor(kwargs[key], **dict([
        build(dep, **kwargs) if isinstance(dep, dict) else
        (_key(dep), dep(kwargs[_key(dep)])) for dep in deps
    ]))


__all__ = [
    'polyfill',
    'iterable',
    'work_path',
    'wrappers',
    #
    'build',
    'load_modules',
]
