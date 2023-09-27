from typing import Dict, List, Any, TypeVar


class Formula:
    def to_file(self, filename: str):
        raise NotImplementedError

    def __iter__(self) -> List[Any]:
        raise NotImplementedError


TFormula = TypeVar('TFormula', bound='Formula')


class Encoding:
    def get_formula(self, copy: bool = True) -> TFormula:
        raise NotImplementedError

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


__all__ = [
    'Encoding',
    # types
    'Formula'
]
