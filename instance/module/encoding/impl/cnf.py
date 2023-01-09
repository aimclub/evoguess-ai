from threading import Lock
from typing import List, Tuple, Dict, Any

from ..encoding import Encoding, EncodingData

from instance.module.variables.vars import Constraints, Supplements

Clause = List[int]
Clauses = List[Clause]

cnf_data = {}
parse_lock = Lock()


class CNFData(EncodingData):
    def __init__(self, clauses: Clauses, lines: str = None, max_lit: int = None):
        self._lines = lines
        self._clauses = clauses
        self._max_lit = max_lit

    def _get_lines_and_max_lit(self) -> Tuple[str, int]:
        if not self._lines or not self._max_lit:
            lines, max_lit = [], 0
            for clause in self._clauses:
                max_lit = max(max_lit, *map(abs, clause))
                lines.append(' '.join(map(str, clause)) + ' 0\n')
            self._lines, self._max_lit = ''.join(lines), max_lit
        return self._lines, self._max_lit

    def _get_source_header(self, payload_len: int) -> str:
        lines, max_lit = self._get_lines_and_max_lit()
        return f'p cnf {max_lit} {len(self._clauses) + payload_len}\n'

    def clauses(self, constraints: Constraints = ()) -> Clauses:
        return [*self._clauses, *constraints]

    def source(self, supplements: Supplements = ((), ())) -> str:
        assumptions, constraints = supplements
        lines, max_lit = self._get_lines_and_max_lit()
        payload_len = len(constraints) + len(assumptions)
        return ''.join([
            self._get_source_header(payload_len),
            lines, *(f'{x} 0\n' for x in assumptions),
            *(' '.join(map(str, c)) + ' 0\n' for c in constraints),
        ])

    @property
    def max_literal(self) -> int:
        return self._get_lines_and_max_lit()[1]


class CNF(Encoding):
    slug = 'encoding:cnf'
    comment_lead = ['p', 'c']

    def __init__(self, from_clauses: Clauses = None, from_file: str = None):
        super().__init__(from_file)
        self.clauses = from_clauses

    def _parse_raw_data(self, raw_data: str):
        process_line = 1
        try:
            lines, clauses, max_lit = [], [], 0
            for line in raw_data.splitlines(keepends=True):
                if line[0] not in self.comment_lead:
                    clause = [int(n) for n in line.split()[:-1]]
                    max_lit = max(max_lit, *map(abs, clause))
                    clauses.append(clause)
                    lines.append(line)
                process_line += 1

            cnf_data[self.filepath] = CNFData(
                clauses, ''.join(lines), max_lit
            )
        except Exception as exc:
            msg = f'Error while parsing encoding file in line {process_line}'
            raise ValueError(msg) from exc

    def _process_raw_data(self):
        with parse_lock:
            if self.filepath in cnf_data:
                return

            data = self.get_raw_data()
            self._parse_raw_data(data)

    def get_data(self) -> CNFData:
        if self.clauses:
            return CNFData(self.clauses)
        elif self.filepath in cnf_data:
            return cnf_data[self.filepath]

        self._process_raw_data()
        return cnf_data[self.filepath]

    def __copy__(self):
        return CNF(
            from_file=self.filepath,
            from_clauses=self.clauses
        )

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'from_file': self.filepath,
            'from_clauses': self.clauses,
        }


__all__ = [
    'CNF',
    'CNFData',
    # types
    'Clause',
    'Clauses'
]
