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
        return get_file_data(self.filepath)

    def __info__(self):
        return {
            'slug': self.slug,
            'from_file': self.filepath,
        }


__all__ = [
    'Encoding',
    'EncodingData'
]
