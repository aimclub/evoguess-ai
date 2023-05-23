from typing import Dict, Any

from ..encoding import Encoding, EncodingData

from typings.searchable import Supplements


class SourceData(EncodingData):
    def __init__(self, lines: str = None):
        self._lines = lines

    def source(self, supplements: Supplements = ((), ())) -> str:
        assumptions, constraints = supplements
        return ''.join([
            self._lines, *(f'{x} 0\n' for x in assumptions),
            *(' '.join(map(str, c)) + ' 0\n' for c in constraints),
        ])

    @property
    def max_literal(self) -> int:
        return 0


class Source(Encoding):
    slug = 'encoding:source'

    def get_data(self) -> SourceData:
        return SourceData(self.get_raw_data())

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'from_file': self.filepath,
        }


__all__ = [
    'Source',
    'SourceData'
]
