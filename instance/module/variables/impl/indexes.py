from typing import Iterable, Dict, Any

from ..vars import Index
from ..variables import Variables
from ..var_tools import parse_indexes


class Indexes(Variables):
    slug = 'variables:indexes'

    def __init__(self, from_iterable: Iterable[int] = None, from_string: str = None):
        self.from_string = from_string
        if from_iterable:
            indexes = list(from_iterable)
            self.from_iterable = indexes
        else:
            self.from_iterable = None
            self.from_string = from_string
            indexes = parse_indexes(from_string)
        super().__init__(from_vars=[Index(i) for i in indexes])

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'from_string': self.from_string,
            'from_iterable': self.from_iterable,
        }


__all__ = [
    'Indexes'
]
