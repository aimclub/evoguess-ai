from pysat import formula as fml
from typing import Any, List, Dict, Optional, Union

from ..encoding import Encoding
from .._readers import PySatReader, CNFReader, \
    CNFPlusReader, WCNFReader, WCNFPlusReader

Clause = List[int]
Clauses = List[Clause]


def wcnf_to_cnf(
        wcnf: fml.WCNF,
        only_hard: bool = True
) -> Union[fml.CNF, fml.CNFPlus]:
    if isinstance(wcnf, fml.WCNFPlus):
        cnf = fml.CNFPlus()
        cnf.atmosts = wcnf.atms
    else:
        cnf = fml.CNF()

    cnf.nv = wcnf.nv
    cnf.clauses = wcnf.hard
    cnf.comments = wcnf.comments
    if not only_hard:
        cnf.clauses += wcnf.soft

    return cnf


class PySatEnc(Encoding):
    slug = 'encoding:pysat'

    def __init__(self, reader: PySatReader):
        self._reader = reader

    def _get_formula(self) -> Any:
        return self._reader.read_formula()

    def _get_formula_flags(self) -> str:
        return 'o'

    def _get_formula_key(self) -> Optional[str]:
        if self._reader and self._reader.from_file:
            flags = self._get_formula_flags()
            slugs = f'{self.slug}#{self._reader.slug}'
            return f'{slugs}#{flags}#{self._reader.from_file}'

    def set_reader(self, reader: PySatReader):
        self._reader = reader
        return self

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            '_reader': self._reader.__config__(),
        }


class CNF(PySatEnc):
    slug = 'encoding:cnf'
    extract_hard = False

    def __init__(
            self,
            from_file: str = None,
            from_string: str = None,
            from_clauses: Clauses = None,
            comment_lead: List[str] = ('c',)
    ):
        super().__init__(CNFReader(
            from_file, from_string, comment_lead
        ) if from_file or from_string else None)
        self.from_clauses = from_clauses

    def _get_formula_flags(self) -> str:
        return 'h' if self.extract_hard \
            else super()._get_formula_flags()

    def _get_formula(self) -> fml.CNF:
        if self.from_clauses:
            return fml.CNF(
                from_clauses=self.from_clauses
            )

        formula = super()._get_formula()
        if isinstance(formula, fml.WCNF):
            return wcnf_to_cnf(
                formula, self.extract_hard
            )
        elif isinstance(formula, fml.CNF):
            return formula

    def weighted(self) -> 'WCNF':
        return WCNF().set_reader(self._reader)

    def __copy__(self) -> 'CNF':
        return CNF(
            from_clauses=self.from_clauses,
        ).set_reader(self._reader)


class CNFPlus(PySatEnc):
    slug = 'encoding:cnf+'
    extract_hard = False

    def __init__(
            self,
            from_file: str = None,
            from_string: str = None,
            comment_lead: List[str] = ('c',)
    ):
        super().__init__(CNFPlusReader(
            from_file, from_string, comment_lead
        ) if from_file or from_string else None)

    def _get_formula_flags(self) -> str:
        return 'h' if self.extract_hard \
            else super()._get_formula_flags()

    def _get_formula(self) -> fml.CNFPlus:
        formula = super()._get_formula()
        if isinstance(formula, fml.WCNFPlus):
            return wcnf_to_cnf(
                formula, self.extract_hard
            )
        elif isinstance(formula, fml.CNFPlus):
            return formula

    def weighted(self) -> 'WCNFPlus':
        return WCNFPlus().set_reader(self._reader)

    def __copy__(self) -> 'CNFPlus':
        return CNFPlus().set_reader(self._reader)


class WCNF(PySatEnc):
    slug = 'encoding:wcnf'

    def __init__(
            self,
            from_file: str = None,
            from_string: str = None,
            comment_lead: List[str] = ('c',)
    ):
        super().__init__(WCNFReader(
            from_file, from_string, comment_lead
        ) if from_file or from_string else None)

    def _get_formula(self) -> fml.WCNF:
        _formula = super()._get_formula()
        if isinstance(_formula, fml.CNF):
            return _formula.weighted()
        elif isinstance(_formula, fml.WCNF):
            return _formula

    def from_hard(self) -> 'CNF':
        cnf = CNF().set_reader(self._reader)
        cnf.extract_hard = True
        return cnf

    def unweighted(self) -> 'CNF':
        return CNF().set_reader(self._reader)

    def __copy__(self) -> 'WCNF':
        return WCNF().set_reader(self._reader)


class WCNFPlus(PySatEnc):
    slug = 'encoding:wcnf+'

    def __init__(
            self,
            from_file: str = None,
            from_string: str = None,
            comment_lead: List[str] = ('c',)
    ):
        super().__init__(WCNFPlusReader(
            from_file, from_string, comment_lead
        ) if from_file or from_string else None)

    def _get_formula(self) -> fml.WCNFPlus:
        _formula = super()._get_formula()
        if isinstance(_formula, fml.CNFPlus):
            return _formula.weighted()
        elif isinstance(_formula, fml.WCNFPlus):
            return _formula

    def from_hard(self) -> 'CNFPlus':
        cnf = CNFPlus().set_reader(self._reader)
        cnf.extract_hard = True
        return cnf

    def unweighted(self) -> 'CNFPlus':
        return CNFPlus().set_reader(self._reader)

    def __copy__(self) -> 'WCNFPlus':
        return WCNFPlus().set_reader(self._reader)


__all__ = [
    'CNF',
    'WCNF',
    'CNFPlus',
    'WCNFPlus',
    # types
    'Clause',
    'Clauses',
    # utility
    'wcnf_to_cnf'
]
