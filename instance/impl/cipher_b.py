from .cipher_s import *

from typing import Optional, List

from ..module.variables.vars import Var
from ..module.encoding.encoding import Encoding
from ..module.variables import Variables, Indexes


class BlockCipher(StreamCipher):
    slug = 'cipher:block'

    def __init__(
            self,
            encoding: Encoding,
            input_set: Indexes,
            plain_set: Indexes,
            output_set: Indexes,
            extra_set: Optional[Variables] = None
    ):
        self.plain_set = plain_set
        super().__init__(encoding, input_set, output_set, extra_set)

    def get_propagation_vars(self) -> List[Var]:
        return [
            *self.plain_set.variables(),
            *super().get_propagation_vars()
        ]

    def get_dependent_vars(self, *args: Variables) -> List[Var]:
        return [
            *self.plain_set.variables(),
            *super().get_dependent_vars(*args)
        ]

    def __info__(self):
        return {
            **super().__info__(),
            'plain_set': self.plain_set.__info__(),
        }


__all__ = [
    'BlockCipher'
]
