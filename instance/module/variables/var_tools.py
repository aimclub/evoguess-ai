import json

from .vars import *
from .vars.var_s import xor, bent4, majority

from typing import Tuple, List
from typings.optional import Int

operations = {
    'xor': xor,
    'bent_4': bent4,
    'majority': majority
}


def parse_range(string: str) -> Tuple[Int, Int]:
    try:
        st, end = string.split('..')
        return int(st), int(end)
    except ValueError:
        return None, None


def parse_indexes(string: str) -> List[int]:
    indexes = []
    # todo: add consistency warnings
    for index in string.split():
        if '..' in index:
            st, end = parse_range(index)
            indexes.extend(range(st, end + 1))
        else:
            indexes.append(int(index))
    return indexes


def parse_vars_raw(vars_raw: str) -> List[Var]:
    variables = []
    # todo: refactor!
    var_scheme = json.loads(vars_raw)
    for key, value in var_scheme.items():
        if key.startswith('index'):
            variables.extend([Index(var) for var in value])
        elif key.startswith('switch'):
            prefix = value['prefix']
            op = operations[value['op']]
            variables.extend([
                Switch(f'{prefix}{i}', group, op)
                for i, group in enumerate(value['groups'])
            ])
        elif key.startswith('domain'):
            prefix = value['prefix']
            variables.extend([
                Domain(f'{prefix}{i}', group)
                for i, group in enumerate(value['groups'])
            ])
            variables.extend([])
        else:
            raise Exception('Unknown variable group key')

    return variables


__all__ = [
    'parse_range',
    'parse_indexes',
    'parse_vars_raw'
]
