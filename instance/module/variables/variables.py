from threading import Lock
from itertools import chain
from typing import Any, List, Dict, Iterable

from .vars import Var, AnyVar
from .var_tools import parse_vars_raw

from util.lazy_file import get_file_data

vars_data = {}
parse_lock = Lock()


def get_var_deps(_vars: Iterable[Var]) -> Iterable[AnyVar]:
    return set(chain(*(v.deps for v in _vars)))


def get_var_bases(_vars: Iterable[AnyVar]) -> List[int]:
    return [2 if isinstance(v, int) else v.base for v in _vars]


class Variables:
    slug = 'variables'

    def __init__(self,
                 from_file: str = None,
                 from_vars: List[Var] = None):
        self._vars = from_vars
        self.filepath = from_file

        self._var_deps = None
        self._var_bases = None
        self._deps_bases = None

    def get_raw_data(self):
        try:
            return get_file_data(self.filepath)
        except FileNotFoundError as exc:
            msg = f'Variables file {self.filepath} not found'
            raise FileNotFoundError(msg) from exc

    def _process_vars_raw(self):
        with parse_lock:
            if self.filepath in vars_data:
                return

            vars_raw = self.get_raw_data()
            vars_data[self.filepath] = parse_vars_raw(vars_raw)

    def variables(self) -> List[Var]:
        if self._vars is not None:
            return self._vars
        elif self.filepath in vars_data:
            return vars_data[self.filepath]

        self._process_vars_raw()
        return vars_data[self.filepath]

    def _upd_var_deps(self):
        self._var_deps = get_var_deps(self.variables())

    def _upd_var_bases(self):
        self._var_bases = get_var_bases(self.variables())

    def _upd_deps_bases(self):
        self._deps_bases = get_var_bases(self.get_var_deps())

    def get_var_deps(self) -> Iterable[AnyVar]:
        if not self._var_deps:
            self._upd_var_deps()
        return self._var_deps

    def get_var_bases(self) -> List[int]:
        if not self._var_bases:
            self._upd_var_bases()
        return self._var_bases

    def get_deps_bases(self) -> List[int]:
        if not self._deps_bases:
            self._upd_deps_bases()
        return self._deps_bases

    def __len__(self):
        return len(self.variables())

    def __contains__(self, item):
        return item in self.variables()

    def __iter__(self):
        return self.variables().__iter__()

    def __hash__(self):
        return hash(tuple(self.variables()))

    def __eq__(self, other):
        # todo: more effective eq
        return str(self) == str(other)

    def __repr__(self):
        return f"[{str(self)}]({len(self)})"

    def __str__(self):
        return ' '.join(map(str, self.variables()))

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'from_file': self.filepath,
            'from_vars': [
                var.__config__() for var in self._vars
            ] if self._vars is not None else None
        }


__all__ = [
    'Var',
    'List',
    'AnyVar',
    'Variables',
    # tools
    'get_var_deps',
    'get_var_bases'
]
