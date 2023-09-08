from pysat import formula
from typing import Any, List, Dict

from ..encoding import Encoding

Clause = List[int]
Clauses = List[Clause]

cnf_data = {}


class CNF(Encoding):
    slug = 'encoding:cnf'

    def __init__(
            self,
            from_file: str = None,
            from_string: str = None,
            from_clauses: Clauses = None,
            comment_lead: List[str] = ('c',)
    ):
        self.from_file = from_file
        self.from_string = from_string
        self.from_clauses = from_clauses
        self.comment_lead = comment_lead

    def get_formula(self) -> formula.CNF:
        if self.from_file is not None:
            if self.from_file not in cnf_data:
                _formula = formula.CNF(
                    from_file=self.from_file,
                    comment_lead=self.comment_lead
                )
                cnf_data[self.from_file] = _formula
            return cnf_data[self.from_file].copy()

        return formula.CNF(
            from_string=self.from_string,
            from_clauses=self.from_clauses,
            comment_lead=self.comment_lead
        )

    def __copy__(self):
        return CNF(
            from_file=self.from_file,
            from_string=self.from_string,
            comment_lead=self.comment_lead,
        )

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'from_file': self.from_file,
            'from_string': self.from_string,
            'from_clauses': self.from_clauses,
            'comment_lead': self.comment_lead
        }


class CNFPlus(CNF):
    slug = 'encoding:cnf+'

    def __init__(
            self,
            from_file: str = None,
            from_string: str = None,
            comment_lead: List[str] = ('c',)
    ):
        super().__init__(
            from_file=from_file,
            from_string=from_string,
            comment_lead=comment_lead
        )

    def get_formula(self) -> formula.CNFPlus:
        if self.from_file is not None:
            if self.from_file not in cnf_data:
                _formula = formula.CNFPlus(
                    from_file=self.from_file,
                    comment_lead=self.comment_lead
                )
                cnf_data[self.from_file] = _formula
            return cnf_data[self.from_file].copy()

        return formula.CNFPlus(
            from_string=self.from_string,
            comment_lead=self.comment_lead
        )

    def __copy__(self):
        return CNFPlus(
            from_file=self.from_file,
            from_string=self.from_string,
            comment_lead=self.comment_lead,
        )


__all__ = [
    'CNF',
    'CNFPlus',
    # types
    'Clause',
    'Clauses'
]
