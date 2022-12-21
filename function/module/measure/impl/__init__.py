from .conflicts import *
from .propagations import *
from .solving_time import *
from .learned_literals import *

measures = {
    Conflicts.slug: Conflicts,
    SolvingTime.slug: SolvingTime,
    Propagations.slug: Propagations,
    LearnedLiterals.slug: LearnedLiterals
}

__all__ = [
    'Conflicts',
    'SolvingTime',
    'Propagations',
    'LearnedLiterals',
]
