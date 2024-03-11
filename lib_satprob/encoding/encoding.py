from typing import Any, Dict, Optional

encoding_data = {}


class EncPatch:
    def apply(self, formula: Any) -> Any:
        raise NotImplementedError


class EncReader:
    slug = None

    def __init__(self, from_file: str):
        self.from_file = from_file

    def read_formula(self) -> Any:
        raise NotImplementedError

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


class Encoding:
    def _get_formula_key(self) -> Optional[str]:
        raise NotImplementedError

    def _get_formula(
            self, patch: EncPatch = None
    ) -> Any:
        raise NotImplementedError

    def get_formula(
            self, copy: bool = True,
            patch: EncPatch = None
    ) -> Any:
        key = self._get_formula_key()
        if key is None or patch is not None:
            return self._get_formula(patch)

        if key not in encoding_data:
            _formula = self._get_formula()
            encoding_data[key] = _formula
        return encoding_data[key].copy() \
            if copy else encoding_data[key]

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


__all__ = [
    'Encoding',
    # utility
    'EncPatch',
    'EncReader'
]
