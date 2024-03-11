import json

from typing import Any, Dict
from tempfile import NamedTemporaryFile

from lib_satprob.problem import Problem
from lib_satprob.encoding import Clauses

FORMULAS: Dict[int, Any] = {}
VERSIONS: Dict[int, Clauses] = {}


class Patch:
    def __init__(self, clauses: Clauses):
        self.clauses = clauses
        self.filename = None
        self.version = None

        self.version = max(VERSIONS.keys()) \
            if len(VERSIONS) > 0 else 1
        VERSIONS[self.version] = clauses

        with NamedTemporaryFile(
                delete=False, mode='w+'
        ) as handle:
            json.dump(clauses, handle)
            self.filename = handle.name

    def get_formula(self, problem: Problem) -> Any:
        if self.version not in FORMULAS:
            # _print('loading...', version, filename)
            formula = problem.encoding.get_formula()
            if self.filename is not None and self.version > 0:
                with open(self.filename, 'r+') as handle:
                    clauses = json.load(handle)
                formula.extend(clauses)

            FORMULAS[self.version] = formula

        return FORMULAS[self.version]


__all__ = [
    'Patch'
]
