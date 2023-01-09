from typing import Dict, Any

from util.lazy_file import get_file_data


class EncodingData:
    def source(self) -> str:
        raise NotImplementedError

    @property
    def max_literal(self) -> int:
        raise NotImplementedError


class Encoding:
    def __init__(self, from_file: str = None):
        self.filepath = from_file

    def get_data(self) -> EncodingData:
        raise NotImplementedError

    def get_raw_data(self) -> str:
        try:
            return get_file_data(self.filepath)
        except FileNotFoundError as exc:
            msg = f'Encoding file {self.filepath} not found'
            raise FileNotFoundError(msg) from exc

    def __config__(self) -> Dict[str, Any]:
        raise NotImplementedError


__all__ = [
    'Encoding',
    'EncodingData'
]
