from pysat import formula
from typing import Any, List, Dict

from ..encoding import EncReader


class PySatReader(EncReader):
    slug = 'reader:pysat'

    def __init__(
            self,
            from_file: str = None,
            from_string: str = None,
            comment_lead: List[str] = ('c',)
    ):
        super().__init__(from_file)
        self.from_string = from_string
        self.comment_lead = comment_lead

    def read_formula(self) -> Any:
        raise NotImplementedError

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'from_file': self.from_file,
            'from_string': self.from_string,
            'comment_lead': self.comment_lead,
        }


class PySatCNFReader(PySatReader):
    slug = 'reader:pysat:cnf'

    def read_formula(self) -> formula.CNF:
        return formula.CNF(
            from_file=self.from_file,
            from_string=self.from_string,
            comment_lead=self.comment_lead
        )


class PySatCNFPlusReader(PySatCNFReader):
    slug = 'reader:pysat:cnf+'

    def read_formula(self) -> formula.CNFPlus:
        return formula.CNFPlus(
            from_file=self.from_file,
            from_string=self.from_string,
            comment_lead=self.comment_lead
        )


class PySatWCNFReader(PySatReader):
    slug = 'reader:pysat:wcnf'

    def read_formula(self) -> formula.WCNF:
        return formula.WCNF(
            from_file=self.from_file,
            from_string=self.from_string,
            comment_lead=self.comment_lead
        )


class PySatWCNFPlusReader(PySatWCNFReader):
    slug = 'reader:pysat:wcnf+'

    def read_formula(self) -> formula.WCNFPlus:
        return formula.WCNFPlus(
            from_file=self.from_file,
            from_string=self.from_string,
            comment_lead=self.comment_lead
        )


__all__ = [
    'PySatCNFReader',
    'PySatWCNFReader',
    'PySatCNFPlusReader',
    'PySatWCNFPlusReader',
    # types
    'PySatReader'
]
