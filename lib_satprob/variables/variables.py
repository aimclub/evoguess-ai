import json

from threading import Lock
from typing import Any, List, Dict, Optional

from ._enum import Enumerable
from .vars import Var, VarMap, \
    var_from, get_var_dims, get_var_sups
from ._utility import Supplements, prod

vars_data = {}
parse_lock = Lock()


class Variables(Enumerable):
    slug = 'variables'

    def __init__(self, from_file: Optional[str] = None,
                 from_vars: Optional[List[Var]] = None):
        self._vars = from_vars
        self.filepath = from_file

        self._var_deps = None
        self._var_bases = None
        self._deps_bases = None

    def _load_from_file(self):
        with parse_lock:
            if self.filepath in vars_data:
                return

            with open(self.filepath) as handle:
                config = json.load(handle)
            if not isinstance(config, list):
                config = config['from_vars']

            _vars = list(map(var_from, config))
            vars_data[self.filepath] = _vars

    def power(self) -> int:
        return prod(self.dimension())

    def variables(self) -> List[Var]:
        if self._vars is not None:
            return self._vars
        elif self.filepath in vars_data:
            return vars_data[self.filepath]

        self._load_from_file()
        return vars_data[self.filepath]

    def dimension(self) -> List[int]:
        if not self._var_bases:
            self._var_bases = list(get_var_dims(self.variables()))
        return self._var_bases

    #
    # def dependents(self) -> List[AnyVar]:
    #     if not self._var_deps:
    #         self._var_deps = list(get_var_deps(self.variables()))
    #     return self._var_deps

    # def get_deps_dims(self) -> List[int]:
    #     if not self._deps_bases:
    #         self._deps_bases = list(get_var_dims(self.get_var_deps()))
    #     return self._deps_bases

    def substitute(self, using_values: Optional[List[int]] = None,
                   using_var_map: Optional[VarMap] = None) -> Supplements:
        return get_var_sups(self._vars, using_var_map, using_values)

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
    'Variables'
]
