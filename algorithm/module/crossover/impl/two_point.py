from typing import Tuple

from ..crossover import *

from instance.module.variables import Backdoor


class TwoPoint(Crossover):
    slug = 'crossover:two-point'

    def cross(self, ind1: Backdoor, ind2: Backdoor) -> Tuple[Backdoor, Backdoor]:
        mask1, mask2 = ind1.get_mask(), ind2.get_mask()

        a = self.random_state.randint(len(mask1))
        b = self.random_state.randint(len(mask2))
        for i in range(min(a, b), max(a, b)):
            mask1[i], mask2[i] = mask2[i], mask1[i]

        return ind1.get_copy(mask1), ind2.get_copy(mask2)


__all__ = [
    'TwoPoint'
]
