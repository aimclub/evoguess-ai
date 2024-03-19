from typing import List
from os import cpu_count
from numpy.random import RandomState

from core.impl import CombineT
from output.impl import CombineLogger

from space.model import Backdoor
from core.model.point import Point

from lib_satprob.solver import Report
from lib_satprob.problem import Problem

from algorithm.impl import MuPlusLambda
from algorithm.module.mutation import FixSize
from algorithm.module.selection import Roulette

from function.module.budget import TaskBudget
from function.module.measure import Conflicts

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

    point = rho_evaluate(initial)
    with algorithm.start(point) as pm:
        for iteration in range(ITER_COUNT):
            backdoor = pm.collect(0, 1)[0]
            point = rho_evaluate(backdoor)
            _, [best, *_] = pm.insert(point)

        return [rho_fn_ext(best.searchable)]


def solve(
        problem: Problem, runs: int, seed_offset: int = 1,
        max_workers: int = 16, bd_size: int = 10,
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

        search_stamp, search_time = time_ms(), passed()
        patch, hard_order = rho_preprocess(all_points, executor)
        pre_stamp, derive_time = time_ms(), passed(search_stamp)
        printc(f'Prepared {len(hard_order)} backdoors')
        phase_1_time = search_time + derive_time

        printc('', 'Phase 2 (Solve problem)')
        measure, budget = Conflicts(), TaskBudget(20000)
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

    return report


__all__ = [
    'solve'
]
