from ..mutation import Mutation

from typings.optional import Int
from instance.module.variables import Backdoor


class Uniform(Mutation):
    slug = 'mutation:uniform'

    def __init__(self, flip_scale: float = 1., random_seed: Int = None):
        self.flip_scale = flip_scale
        super().__init__(random_seed)

    def mutate(self, individual: Backdoor) -> Backdoor:
        mask = individual.get_mask()
        prob = self.flip_scale / len(mask)

        # todo: move _distribution to tool funcs
        distribution = self._distribution(prob, len(mask))
        for i, value in enumerate(distribution):
            if prob > value:
                mask[i] = not mask[i]

        return individual.get_copy(mask)

    def __info__(self):
        return {
            **super().__info__(),
            'flip_scale': self.flip_scale
        }


__all__ = [
    'Uniform'
]
