from typing import Dict, Any

from . import impl
from .impl import *
from .comparator import Comparator

impls = impl.comparators


def comparator_from(config: Dict[str, Any]) -> Comparator:
    slug = config.pop('slug')
    return impls[slug](**config)


__all__ = [
    'Comparator',
    *impl.__all__
]
