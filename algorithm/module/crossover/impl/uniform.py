from typing import Tuple

from ..crossover import *

from typings.optional import Int
from instance.module.variables import Backdoor


class Uniform(Crossover):
    slug = 'crossover:uniform'

    def __init__(self, swap_prob: float = 0.5, random_seed: Int = None):
        self.swap_prob = swap_prob
        super().__init__(random_seed)

    def cross(self, ind1: Backdoor, ind2: Backdoor) -> Tuple[Backdoor, Backdoor]:
        mask1, mask2 = ind1.get_mask(), ind2.get_mask()

        # todo: use _distribution from tool funcs
        distribution = self.random_state.rand(len(mask1))
        for i, value in enumerate(distribution):
            if self.swap_prob >= value:
                mask1[i], mask2[i] = mask2[i], mask1[i]

        return ind1.get_copy(mask1), ind2.get_copy(mask2)

    def __info__(self):
        return {
            **super().__info__(),
            'swap_prob': self.swap_prob
        }


__all__ = [
    'Uniform'
]
