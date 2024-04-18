from typing import List, Optional, NamedTuple

from core.model.point import Point

from lib_satprob.derived import get_derived_by
from lib_satprob.variables import Supplements
from lib_satprob.encoding.patch import SatPatch

from utility.polyfill import tqdm
from utility.iterable import split_by


def derive(_point: Point) -> Supplements:
    _easy_cubes = get_easy_cubes(_point)
    return get_derived_by(_easy_cubes)


def get_easy_cubes(point: Point) -> List[Supplements]:
    power = point.searchable.power()
    nums, easy = point.get('hard_nums'), []
    return list(point.searchable.enumerate([
        i for i in range(power) if i not in nums
    ]))


def get_hard_cubes(point: Point) -> List[Supplements]:
    return list(point.searchable.enumerate(
        point.get('hard_nums')
    ))


class RhoPreprocessed(NamedTuple):
    sat_patch: Optional[SatPatch]
    hard_order: List[List[Supplements]]


def rho_preprocess(
        points: List[Point], executor=None, units: set = None,
) -> RhoPreprocessed:
    all_assumptions, all_constraints = set(), set()
    point_order, current_var_set = [], set()
    # проверяем unit_lits на контрарность (тогда задача ансат) и фильтруем от повторов
    all_assumptions.update(set(units))
    current_var_set.update(set(map(abs, units)))

    def var_distance(_point: Point) -> int:
        return sum([
            0 if _var.index in current_var_set else 1
            for _var in _point.searchable.variables()
        ])

    def is_one_hard(point: Point) -> bool:
        return point.get('hard') == 1

    # separate single hard points from other
    single_hard, points = split_by(points, is_one_hard)
    points = sorted(points, key=lambda p: p.get('hard'))

    def add_point_to_order(_point: Point):
        point_order.append(_point)
        _backdoor = _point.searchable
        for _var in _backdoor.variables():
            current_var_set.add(_var.index)

    def add_supplements(_supplements: Supplements):
        _assumptions, _constraints = _supplements
        all_assumptions.update(set(_assumptions))
        for _clause in map(tuple, _constraints):
            all_constraints.add(_clause)
        for _index in map(abs, _assumptions):
            current_var_set.add(_index)


    # add single hard like assumptions
    for point in single_hard:
        print('blabla')
        backdoor = point.searchable
        num = point.get('hard_nums')[0]
        sups = backdoor.enumerate([num])
        add_supplements(next(sups))

    # derive supplements from other points
    points = list(filter(var_distance, points))
    derive_map = executor.map if executor else map

    desc, total, unit = 'Deriving', len(points), 'bd'
    with tqdm(total, desc=desc, unit=unit) as progress:
        for supplements in derive_map(derive, points):
            progress.update()
            add_supplements(supplements)

            c_len = len(all_constraints)
            a_len = len(all_assumptions)
            progress.set_postfix_str(
                f'{a_len + c_len} clauses'
            )

    # init point order list
    if len(current_var_set) == 0:
        point = points.pop(0)
        add_point_to_order(point)

    # build point order strategy
    while len(points) > 0:
        next_point = (None, 0)
        for point in points:
            distance = var_distance(point)
            if distance > next_point[1]:
                next_point = (point, distance)

        point, _ = next_point
        add_point_to_order(point)

        # exclude points with zero distance
        points = list(filter(var_distance, points))

    # extract hard tasks from points in order
    hard_order = map(get_hard_cubes, point_order)
    # finalize additional clauses list
    constraints = list(map(list, all_constraints))
    clauses = constraints + [[a] for a in all_assumptions]
    sat_patch = SatPatch(clauses) if len(clauses) else None
    return RhoPreprocessed(sat_patch, list(hard_order))


__all__ = [
    'rho_preprocess',
    'RhoPreprocessed'
]
