import json

from os import path, remove
from typing import Any, Dict, List
from tempfile import NamedTemporaryFile

from ..encoding import EncPatch
from ...variables import Clauses

PATCHES: Dict[str, Any] = {}


class SatPatch(EncPatch):
    def __init__(self, clauses: Clauses):
        self._filename = None

        with NamedTemporaryFile(
                delete=False, mode='w+'
        ) as handle:
            json.dump(clauses, handle)
            self._filename = handle.name

    def _load(self) -> Clauses:
        if self._filename is None:
            raise FileNotFoundError

        if self._filename not in PATCHES:
            with open(self._filename) as handle:
                clauses = json.load(handle)
            PATCHES[self._filename] = clauses

        return PATCHES[self._filename]

    @property
    def clauses(self) -> Clauses:
        return self._load()

    def apply(self, formula: Any) -> Any:
        formula.extend(self._load())
        return formula

    def __eq__(self, other: 'SatPatch') -> bool:
        if other and isinstance(other, SatPatch):
            return self._filename == other._filename

    def __del__(self):
        if path.exists(self._filename):
            remove(self._filename)


__all__ = [
    'SatPatch'
]
