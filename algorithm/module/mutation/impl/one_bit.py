from ..mutation import Mutation

from instance.module.variables import Backdoor


class OneBit(Mutation):
    slug = 'mutation:one-bit'

    def mutate(self, individual: Backdoor) -> Backdoor:
        mask = individual.get_mask()
        i = self.random_state.randint(0, len(mask))

        mask[i] = not mask[i]
        return individual.get_copy(mask)


__all__ = [
    'OneBit'
]
