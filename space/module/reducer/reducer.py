from instance import Instance

from instance.module.variables import Variables


class Reducer:
    def reduce(self, instance: Instance, variables: Variables) -> Variables:
        raise NotImplementedError


__all__ = [
    'Reducer'
]
