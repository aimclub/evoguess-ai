from .roulette import *
from .best_point import *
# from .tournament import *

selections = {
    Roulette.slug: Roulette,
    BestPoint.slug: BestPoint,
    # Tournament.slug: Tournament
}

__all__ = [
    'BestPoint',
    'Roulette',
    # 'Tournament'
]
