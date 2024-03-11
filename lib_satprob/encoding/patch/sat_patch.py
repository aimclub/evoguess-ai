import json

from os import path, remove
from typing import Any, Dict, List
from tempfile import NamedTemporaryFile

from ..encoding import EncPatch

FORMULAS: Dict[str, Any] = {}


class SatPatch(EncPatch):
    def __init__(self, clauses: List[List[int]]):
        self.clauses = clauses
        self._filename = None

        with NamedTemporaryFile(
                delete=False, mode='w+'
        ) as handle:
            json.dump(clauses, handle)
            self._filename = handle.name

    def apply(self, formula: Any) -> Any:
        if self._filename is None:
            raise FileNotFoundError

        if self._filename not in FORMULAS:
            # print('loading...', self._filename)
            with open(self._filename, 'r+') as handle:
                clauses = json.load(handle)
            formula.extend(clauses)

            FORMULAS[self._filename] = formula

        return FORMULAS[self._filename]

    def __del__(self):
        # print('del', self._filename)
        if path.exists(self._filename):
            remove(self._filename)


__all__ = [
    'SatPatch'
]
