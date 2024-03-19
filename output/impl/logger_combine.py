import json
from typing import TYPE_CHECKING

from ..abc import Logger

from lib_satprob.solver import Report
from lib_satprob.problem import Problem

from utility.work_path import WorkPath

if TYPE_CHECKING:
    from core.model.point import Point


class CombineLogger(Logger):
    solution_counter = 1
    slug = 'logger:combine'

    def __init__(self, out_path: WorkPath):
        super().__init__(out_path)
        self._solution_counter = 1

    def meta(self, problem: Problem, *points: 'Point') -> Logger:
        return self._write(json.dumps([
            problem.__config__(), *(
                point.__config__()
                for point in points
            )], indent=2), 'meta.json')

    def write(self, solution: Report, spent: float) -> Logger:
        if solution.model is not None:
            index = self._solution_counter
            _, _, model, cost = solution
            self._solution_counter += 1
            return self._format({
                'index': index, 'spent': spent,
                'cost': cost, 'model': model,
            }, filename='solutions.jsonl')


__all__ = [
    'CombineLogger'
]
