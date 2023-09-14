import json
from base64 import b85decode
from typing import Any, Dict, Iterable, NamedTuple, Tuple, Callable

from ..abc import Parser

from space.model import Backdoor
from typings.searchable import Searchable
from core.model.point import Point, PointSet
from core.module.comparator import Comparator, comparator_from
from pysatmc.variables import variables_from


class Iteration(NamedTuple):
    index: int
    spent: float
    points: PointSet


def get_deserialize(backdoor: Searchable, comparator: Comparator) -> Callable:
    def deserialize(point: Dict[str, Any]) -> Point:
        mask = Searchable.unpack(b85decode(point['backdoor']))
        return Point(
            backdoor=backdoor.make_copy(mask),
            comparator=comparator
        ).set(**point['estimation'])

    return deserialize


class OptimizeParser(Parser):
    slug = 'parser:optimize'

    def meta(self) -> Tuple[Searchable, Comparator]:
        [initial, comparator] = self._read_json('meta.json')
        backdoor = Backdoor(variables=variables_from(initial))
        return backdoor, comparator_from(comparator)

    def parse(self, *args, **kwargs) -> Iterable[Iteration]:
        deserialize = get_deserialize(*self.meta())
        for data in map(json.loads, self.read(filename='log.jsonl')):
            yield Iteration(data['index'], data['spent'], [
                deserialize(point) for point in data['points']
            ])


__all__ = [
    'OptimizeParser'
]
