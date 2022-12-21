from ..limitation import *


class Iteration(Limitation):
    key = 'iteration'
    slug = 'limitation:iteration'

    def __config__(self):
        return {
            'slug': self.slug,
            'value': self.limit
        }


__all__ = [
    'Iteration'
]
