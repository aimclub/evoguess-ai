from typing import List, Tuple

from .cnf import CNF, CNFData, Clause, Clauses

Atmost = Tuple[List[int], int]
Atmosts = List[Atmost]

cnfp_data = {}


class CNFPData(CNFData):
    def __init__(self, clauses: Clauses, atmosts: Atmosts, *args, **kwargs):
        self._atmosts = atmosts
        super().__init__(clauses, *args, **kwargs)

    def _get_lines_and_max_lit(self) -> Tuple[str, int]:
        if not self._lines or not self._max_lit:
            lines, max_lit = [], 0
            for clause in self._clauses:
                max_lit = max(max_lit, *map(abs, clause))
                lines.append(' '.join(map(str, clause)) + ' 0\n')
            for atmost in self._atmosts:
                literals, rhd = atmost
                lines.append(' '.join(map(str, literals)) + f' <= {rhd}\n')
            self._lines, self._max_lit = ''.join(lines), max_lit
        return self._lines, self._max_lit

    def _get_source_header(self, payload_len: int) -> str:
        lines, max_lit = self._get_lines_and_max_lit()
        return f'p cnf {max_lit} {len(self._clauses) + payload_len}\n' if not self.atmosts \
            else f'p cnf+ {max_lit} {len(self._clauses) + len(self._atmosts) + payload_len}\n'

    def atmosts(self) -> Atmosts:
        return self._atmosts


class CNFP(CNF):
    slug = 'encoding:cnf+'

    def __init__(self, from_clauses: Clauses = None,
                 from_atmosts: Atmosts = None, from_file: str = None):
        super().__init__(from_clauses, from_file)
        self.atmosts = from_atmosts

    def _parse_raw_data(self, raw_data: str):
        lines, clauses, atmosts, max_lit = [], [], [], 0
        for line in raw_data.splitlines(keepends=True):
            if line[0] not in self.comment_lead:
                if int(line.rsplit(' ', 1)[-1]) == 0:
                    clause = [int(n) for n in line.split()[:-1]]
                    max_lit = max(max_lit, *map(abs, clause))
                    clauses.append(clause)
                else:
                    items = [i for i in line.split()]
                    if items[-2][0] == '>':
                        lits = [-int(n) for n in items[:-2]]
                        rhs = len(lits) - int(items[-1])
                    else:
                        rhs = int(items[-1])
                        lits = [int(n) for n in items[:-2]]
                    max_lit = max(max_lit, *map(abs, lits))
                    atmosts.append((lits, rhs))
                lines.append(line)

        cnfp_data[self.filepath] = CNFPData(
            clauses, atmosts, ''.join(lines), max_lit
        )

    def get_data(self) -> CNFPData:
        if self.clauses:
            return CNFPData(self.clauses, self.atmosts)
        elif self.filepath in cnfp_data:
            return cnfp_data[self.filepath]

        self._process_raw_data()
        return cnfp_data[self.filepath]

    def __copy__(self):
        return CNFP(
            from_file=self.filepath,
            from_clauses=self.clauses,
            from_atmosts=self.atmosts,
        )

    def __info__(self):
        return {
            **super().__info__(),
            'from_atmosts': self.atmosts,
        }


__all__ = [
    'CNFP',
    'CNFPData',
    # types
    'Atmost',
    'Atmosts',
]
