from typing import Any, Dict, TypeVar

from .impl import *
from .encoding import *
from . import impl, encoding

impls = impl.encodings

TEncoding = TypeVar('TEncoding', bound='Encoding')


def encoding_from(config: Dict[str, Any]) -> TEncoding:
    slug = config.pop('slug')
    return impls[slug](**config)

__all__ = [
    *impl.__all__,
    *encoding.__all__,
    # from loader
    'encoding_from',
]
