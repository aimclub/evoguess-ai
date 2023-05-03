from typings.optional import Int
from ..mutation import Mutation

from util.iterable import to_bin, from_bin

from typings.optional import Int
from typings.searchable import Searchable


class LogDiv(Mutation):
    slug = 'mutation:log-div'

    def __init__(self, max_noise_scale: float = 0.5, random_seed: Int = None):
        self.max_noise_scale = max_noise_scale
        super().__init__(random_seed)

    def mutate(self, individual: Searchable) -> Searchable:
        vector = individual.get_vector()
        number = from_bin(vector, len(vector)) // 2

        scale = self.random_state.rand()
        noise = number * self.max_noise_scale * scale
        vector = to_bin(int(number + noise), len(vector))
        return individual.make_copy(vector)


__all__ = [
    'LogDiv'
]
