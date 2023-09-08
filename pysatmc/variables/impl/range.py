from typing import Dict, Any

from .indexes import Indexes, parse_range


class Range(Indexes):
    slug = 'variables:range'

    def __init__(
            self,
            start: int = None,
            length: int = None,
            from_string: str = None
    ):
        self.start, self.length = start, length
        if from_string:
            super().__init__(from_string=from_string)
            self.start, self.end = parse_range(from_string)
        else:
            self.end = self.start + self.length - 1
            super().__init__(from_iterable=range(self.start, self.end + 1))

    def __str__(self):
        return f'{self.start}..{self.end}'

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'start': self.start,
            'length': self.length,
            'from_string': self.from_string,
        }


__all__ = [
    'Range'
]
