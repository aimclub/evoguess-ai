from math import ceil
from typing import List, Tuple, Dict, Any

from function.models import Results, ChunkOffset, ChunkLength

SampleChunk = Tuple[ChunkOffset, ChunkLength]


class SamplingState:
    def __init__(self, sampling: 'Sampling', offset: int, size: int):
        self.size = size
        self.offset = offset
        self.sampling = sampling

    def chunks(self, results: Results) -> List[SampleChunk]:
        count = self.sampling.get_count(self.offset, self.size, results)
        sample_chunks, chunk_size = [], self.sampling.split_into
        chunk_count, remainder = divmod(count, chunk_size)
        for chunk_i in range(0, chunk_count):
            sample_chunks.append((self.offset, chunk_size))
            self.offset += chunk_size
        if remainder > 0:
            sample_chunks.append((self.offset, remainder))
            self.offset += remainder
        return sample_chunks


class Sampling:
    slug = 'sampling'

    def __init__(self, max_size: int, split_into: int):
        self.max_size = max_size
        self.split_into = split_into

    def summarize(self, results: Results) -> Dict[str, Any]:
        raise NotImplementedError

    def get_state(self, offset: int, size: int) -> SamplingState:
        return SamplingState(self, offset, size)

    def get_count(self, offset: int, size: int, results: Results) -> int:
        raise NotImplementedError

    @property
    def max_chunks(self) -> int:
        return ceil(self.max_size / self.split_into)

    def __str__(self):
        return self.slug


__all__ = [
    'Sampling',
    # types
    'SampleChunk',
    'SamplingState',
]
