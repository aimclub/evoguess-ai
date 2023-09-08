from typing import Dict, List, Any


class Formula:
    def to_file(self, filename: str):
        raise NotImplementedError

    def __iter__(self) -> List[Any]:
        raise NotImplementedError


class Encoding:
    def get_formula(self) -> Formula:
        raise NotImplementedError

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


__all__ = [
    'Encoding',
    # types
    'Formula'
]
