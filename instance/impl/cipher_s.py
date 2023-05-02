from .instance import *

from typing import Optional, List

from ..module.variables.vars import Var
from ..module.encoding.encoding import Encoding
from ..module.variables import Variables, Indexes


class StreamCipher(Instance):
    slug = 'cipher:stream'
    input_dependent = True

    def __init__(
            self,
            encoding: Encoding,
            input_set: Indexes,
            output_set: Variables,
            extra_set: Optional[Variables] = None
    ):
        super().__init__(encoding)
        self.input_set = input_set
        self.output_set = output_set
        self.extra_set = extra_set or Variables(from_vars=[])

    def get_dependent_vars(self) -> List[Var]:
        return [
            *self.extra_set.variables(),
            *self.output_set.variables()
        ]

    def get_propagation_vars(self) -> List[Var]:
        return self.input_set.variables()

    # def __info__(self):
    #     return {
    #         **super().__info__(),
    #         'input_set': self.input_set.__info__(),
    #         'extra_set': self.extra_set.__info__(),
    #         'output_set': self.output_set.__info__(),
    #     }


__all__ = [
    'StreamCipher',
]
