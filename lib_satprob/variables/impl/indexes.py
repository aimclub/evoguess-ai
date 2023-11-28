from typing import Any, Dict, Tuple, Iterable

from ..vars import Index
from ..variables import Variables


def parse_range(string: str) -> Tuple[int, int]:
    st, end = string.split('..')
    return int(st), int(end)


def parse_indexes(string: str) -> Iterable[int]:
    for index in string.split():
        if '..' in index:
            st, end = parse_range(index)
            yield from range(st, end + 1)
        else:
            yield int(index)


class Indexes(Variables):
    slug = 'variables:indexes'

    def __init__(
            self,
            from_string: str = None,
            from_iterable: Iterable[int] = None
    ):
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
    'Indexes',
    # utils
    'parse_range',
    'parse_indexes'
]
