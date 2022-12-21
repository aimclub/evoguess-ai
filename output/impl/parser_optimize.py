import json
from base64 import b85decode
from typing import Any, Dict, Iterable, NamedTuple, Tuple, Callable

from ..abc import Parser

from core.model.point import Point, Vector
from core.module.comparator import Comparator, comparator_from
from instance.module.variables import Backdoor, variables_from


class Iteration(NamedTuple):
    index: int
    spent: float
    points: Vector


def get_deserialize(backdoor: Backdoor, comparator: Comparator) -> Callable:
    def deserialize(point: Dict[str, Any]) -> Point:
        mask = Backdoor.unpack(b85decode(point['backdoor']))
        return Point(
            backdoor=backdoor.get_copy(mask),
            comparator=comparator
        ).set(**point['estimation'])

    return deserialize


class OptimizeParser(Parser):
    slug = 'parser:optimize'

    def meta(self) -> Tuple[Backdoor, Comparator]:
        [initial, comparator] = self._read_json('meta.json')
        return variables_from(initial), comparator_from(comparator)

    def parse(self, *args, **kwargs) -> Iterable[Iteration]:
        deserialize = get_deserialize(*self.meta())
        for data in map(json.loads, self.read(filename='log.jsonl')):
            yield Iteration(data['index'], data['spent'], [
                deserialize(point) for point in data['points']
            ])


__all__ = [
    'OptimizeParser'
]
