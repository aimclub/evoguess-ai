from typing import List
from os import cpu_count
from numpy.random import RandomState

from core.impl import CombineT
from function.module.measure import Measure
from output.impl import CombineLogger

from space.model import Backdoor
from core.model.point import Point

from lib_satprob.solver import Report
from lib_satprob.problem import Problem

from algorithm.impl import MuPlusLambda
from algorithm.module.mutation import FixSize
from algorithm.module.selection import Roulette

from function.module.budget import TaskBudget

from rho_tool import rho_fn, rho_fn_ext
from rho_tool.rho_pool import \
    init_process_pool, get_process_state
from rho_tool.rho_order import rho_preprocess

from utility.polyfill import tqdm
from utility.work_path import WorkPath
from utility.format import printc, passed, time_ms

MU_SIZE = 1
LAMBDA_SIZE = 1
ITER_COUNT = 3000


def rho_evaluate(backdoor: Backdoor) -> Point:
    cache = get_process_state().cache

    key = str(backdoor)
    point = cache.get(key)
    if point is not None:
        return point

    point = rho_fn(backdoor)
    cache[key] = point
    return point


def run_alg(size: int, seed: int) -> List[Point]:
    state = RandomState(seed=seed)
    mo_seed = state.randint(2 ** 31)
    so_seed = state.randint(2 ** 31)

    algorithm = MuPlusLambda(
        MU_SIZE, LAMBDA_SIZE,
        selection=Roulette(so_seed),
        mutation=FixSize(size, mo_seed)
    )

    space = get_process_state().space
    vector = state.randint(0, 2, size)
    initial = space._get_searchable()
    initial._set_vector(list(vector))

    best_value, point = 1, rho_evaluate(initial)
    same_value = {str(point.searchable): point}
    with algorithm.start(point) as pm:
        # import os
        for iteration in range(ITER_COUNT):
            backdoor = pm.collect(0, 1)[0]
            point = rho_evaluate(backdoor)
            # print(f'PID: {os.getpid()}, iter {iteration} of {range(ITER_COUNT)}, point {point}')
            _, population = pm.insert(point)
            # TODO гдето тут надо апдейтить пространство поиска если 1 хард таска
            for point in population:
                _value = point.get('value')
                _key = str(point.searchable)
                if _value == best_value:
                    if _key not in same_value:
                        same_value[_key] = point
                elif _value < best_value:
                    same_value = {_key: point}
                    best_value = _value

        return [
            rho_fn_ext(point.searchable)
            for point in same_value.values()
        ]


def solve(
        problem: Problem, runs: int, measure: Measure,
        seed_offset: int = 1,
        max_workers: int = 16, bd_size: int = 10,
        limit: int = 20000,
        log_path: WorkPath = None
) -> Report:
    dirs = ('examples', 'logs', 'rho_solve')
    log_path = log_path or WorkPath(*dirs)

    with CombineLogger(log_path) as logger:
        workers = min(cpu_count(), max_workers)
        printc(f'Running on {workers} threads')
        executor = init_process_pool(problem, workers)

        printc('', 'Phase 1 (Prepare backdoors)')
        all_points, tqdm_kwargs = [], {
            'unit': 'run', 'postfix': '0 bds',
            'desc': 'Searching', 'total': runs
        }
        with tqdm(**tqdm_kwargs) as progress:
            for points in executor.map(run_alg, *zip(*(
                    (bd_size, seed_offset + seed)
                    for seed in range(runs)
            ))):
                progress.update()
                all_points.extend(points)
                progress.set_postfix_str(
                    f'{len(all_points)} bds'
                )
            logger.meta(problem, *all_points)
        # for el in sorted(all_points):
            # print(el)
        search_stamp, search_time = time_ms(), passed()
        patch, hard_order = rho_preprocess(all_points, executor)
        pre_stamp, derive_time = time_ms(), passed(search_stamp)
        printc(f'Prepared {len(hard_order)} backdoors')
        # print(hard_order)

        phase_1_time = search_time + derive_time

        printc('', 'Phase 2 (Solve problem)')
        budget = TaskBudget(limit)
        combine = CombineT(logger, problem, measure, budget)
        report = combine.process(patch, hard_order, executor)
        phase_2_time = passed(pre_stamp)

    if report.status is False:
        printc('', 'Solution', 'UNSATISFIABLE', '')
    elif report.model is not None:
        model_size = len(report.model)
        printc('', 'Solution', 'SATISFIABLE')
        printc(f'Found {model_size} solutions')

    printc(f'Search time: {search_time} sec.')
    printc(f'Derive time: {derive_time} sec.')
    printc(f'Solving time: {phase_2_time} sec.')

    sum_time = round(phase_1_time + phase_2_time, 2)
    printc('', f'Summary time: {sum_time} sec.')

    return Report(report.status, {
        **report.stats,
        'sum_time': sum_time
    }, report.model, report.cost)


__all__ = [
    'solve'
]
