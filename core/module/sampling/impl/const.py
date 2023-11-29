from typing import Dict, Any

from ..sampling import Sampling
from function.model import Results


class Const(Sampling):
    slug = 'sampling:const'

    def __init__(self, size: int, split_into: int):
        super().__init__(size, split_into)

    def summarize(self, results: Results) -> Dict[str, Any]:
        return {}

    def get_count(self, offset: int, size: int, results: Results) -> int:
        return max(0, min(self.max_size, size) - offset)

    def __config__(self):
        return {
            'slug': self.slug,
            'size': self.max_size,
            'split_into': self.split_into
        }


__all__ = [
    'Const'
]
