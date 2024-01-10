from typing import List

from lib_satprob.variables import Indexes

from .backdoor import Backdoor


def load_backdoors(from_file: str) -> List[Backdoor]:
    with open(from_file) as _handle:
        return [
            Backdoor(Indexes(from_string=bd_line))
            for bd_line in _handle.readlines()
        ]


__all__ = [
    'load_backdoors'
]
