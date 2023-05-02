from enum import Enum
from typing import NamedTuple, Tuple, Dict, List


class Status(Enum):
    [
        SOLVED,  # in SAT solvers it usually defines UNSAT
        RESOLVED,  # in SAT solvers it usually defines SAT
        EXHAUSTED,  # if measure budget limit exhausted
        NOT_REACHED,  # if at least measure limit didn't reach
        INTERRUPTED,  # in SAT solvers it always defines INDET
    ] = range(5)

    def __hash__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        return super().__eq__(other)


SampleSeed = int
SampleSize = int
ChunkOffset = int
ChunkLength = int

WorkerArgs = Tuple[
    SampleSeed,
    SampleSize,
    ChunkOffset,
    ChunkLength
]

ProcessId = int
ProcessTime = float

TimeMap = Dict[Status, float]
ValueMap = Dict[Status, float]
StatusMap = Dict[Status, int]

WorkerResult = Tuple[
    ProcessId,
    ProcessTime,
    # main info
    TimeMap,
    ValueMap,
    StatusMap,
    WorkerArgs,
]


class ChunkResult(NamedTuple):
    pid: ProcessId
    ptime: ProcessTime
    # main info
    times: TimeMap
    values: ValueMap
    statuses: StatusMap
    arguments: WorkerArgs


Results = List[ChunkResult]

__all__ = [
    'Status',
    'Results',
    'TimeMap',
    'ValueMap',
    'StatusMap',
    'WorkerArgs',
    'ChunkResult',
    'WorkerResult',
    # workers args
    'ChunkOffset',
    'ChunkLength'
]
