from pysat import formula
from typing import Any, List, Dict

from ..encoding import Encoding

wcnf_data = {}


class WCNF(Encoding):
    slug = 'encoding:wcnf'

    def __init__(
            self,
            from_file: str = None,
            from_string: str = None,
            comment_lead: List[str] = ('c',)
    ):
        self.from_file = from_file
        self.from_string = from_string
        self.comment_lead = comment_lead

    def get_formula(self, copy: bool = True) -> formula.WCNF:
        if self.from_file is not None:
            if self.from_file not in wcnf_data:
                _formula = formula.WCNF(
                    from_file=self.from_file,
                    comment_lead=self.comment_lead
                )
                wcnf_data[self.from_file] = _formula
            return wcnf_data[self.from_file].copy() if \
                copy else wcnf_data[self.from_file]

        return formula.WCNF(
            from_string=self.from_string,
            comment_lead=self.comment_lead
        )

    def __copy__(self):
        return WCNF(
            from_file=self.from_file,
            from_string=self.from_string,
            comment_lead=self.comment_lead,
        )

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'from_file': self.from_file,
            'from_string': self.from_string,
            'comment_lead': self.comment_lead
        }


class WCNFPlus(WCNF):
    slug = 'encoding:wcnf+'

    def get_formula(self) -> formula.WCNFPlus:
        if self.from_file is not None:
            if self.from_file not in wcnf_data:
                _formula = formula.WCNFPlus(
                    from_file=self.from_file,
                    comment_lead=self.comment_lead
                )
                wcnf_data[self.from_file] = _formula
            return wcnf_data[self.from_file].copy()

        return formula.WCNFPlus(
            from_string=self.from_string,
            comment_lead=self.comment_lead
        )

    def __copy__(self):
        return WCNFPlus(
            from_file=self.from_file,
            from_string=self.from_string,
            comment_lead=self.comment_lead,
        )


__all__ = [
    'WCNF',
    'WCNFPlus'
]
