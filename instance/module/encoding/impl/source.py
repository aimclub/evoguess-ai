from typing import Dict, Any

from ..encoding import Encoding, EncodingData

from typings.searchable import Supplements


class SourceData(EncodingData):
    def __init__(self, lines: str = None):
        line, tail = lines.split('\n', maxsplit=1)
        if line.startswith('p'):
            parts = line.split()
            self._lines = tail
            self.max_lit = int(parts[2])
            self.clauses = int(parts[3])
        else:
            self._lines = lines
            self.max_lit = 0
            self.clauses = 0

    def source(self, supplements: Supplements = ((), ())) -> str:
        assumptions, constraints = supplements
        clauses = self.clauses + len(constraints) + len(assumptions)
        header = f'p cnf {self.max_lit} {clauses}\n' if self.clauses else ''
        return ''.join([
            header, self._lines, *(f'{x} 0\n' for x in assumptions),
            *(' '.join(map(str, c)) + ' 0\n' for c in constraints),
        ])

    @property
    def max_literal(self) -> int:
        return self.max_lit


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
