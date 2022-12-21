from typing import Dict, Any

from ..space import Space

from instance.impl import StreamCipher
from instance.module.variables import Backdoor, make_backdoor


class InputSet(Space):
    slug = 'space:input_set'

    # noinspection PyProtectedMember
    def get_backdoor(self, cipher: StreamCipher) -> Backdoor:
        return make_backdoor(cipher.input_set)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'by_mask': self.by_mask,
            'by_string': self.by_string
        }


__all__ = [
    'InputSet'
]
