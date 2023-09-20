from pysatmc.problem import Problem
from pysatmc.variables import Variables


class Reducer:
    def reduce(self, problem: Problem, variables: Variables) -> Variables:
        raise NotImplementedError


__all__ = [
    'Reducer'
]
