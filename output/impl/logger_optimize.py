import json
from base64 import b85encode
from typing import Any, Dict, Tuple

from ..abc import Logger

from core.model.point import Vector, Point
from core.module.comparator import Comparator
from instance.module.variables import Backdoor


def serialize(point: Point) -> Dict[str, Any]:
    return {
        'estimation': point.estimation,
        'backdoor': b85encode(point.backdoor.pack()).decode("utf-8"),
    }


class OptimizeLogger(Logger):
    slug = 'logger:optimize'

    def meta(self, initial: Backdoor, comparator: Comparator) -> Logger:
        return self._write(json.dumps([
            initial.__config__(),
            comparator.__config__()
        ], indent=2), 'meta.json')

    def write(self, insertion: Tuple[int, Vector], spent: float) -> Logger:
        if insertion is not None:
            index, vector = insertion
            return self._format({
                'index': index, 'spent': round(spent, 2),
                'points': list(map(serialize, vector))
            }, filename='log.jsonl')


__all__ = [
    'OptimizeLogger'
]
