from lib_satprob.problem import Problem
from lib_satprob.variables import Variables


class Reducer:
    def reduce(self, problem: Problem, variables: Variables) -> Variables:
        raise NotImplementedError


__all__ = [
    'Reducer'
]
