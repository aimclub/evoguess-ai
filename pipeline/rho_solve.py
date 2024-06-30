from os import cpu_count
from numpy.random import RandomState
from typing import Set, List, NamedTuple, Optional
from concurrent.futures import wait, FIRST_COMPLETED

from core.impl import CombineT
from space.model import Backdoor
from core.model.point import Point
from output.impl import CombineLogger

from lib_satprob.solver import Report
from lib_satprob.problem import Problem

from algorithm.impl import MuPlusLambda
from algorithm.module.mutation import FixSize
from algorithm.module.selection import Roulette

from function.module.measure import Measure
from function.module.budget import TaskBudget

from rho_tool import rho_fn, rho_fn_ext
from rho_tool.rho_pool import \
    init_process_pool, get_process_state
from rho_tool.rho_order import rho_preprocess

from utility.polyfill import tqdm
from utility.work_path import WorkPath
from utility.format import printc, passed, time_ms

MU_SIZE = 1
MIN_RHO = 0.85
LAMBDA_SIZE = 1

OptWorkPath = Optional[WorkPath]


class SearchResult(NamedTuple):
    literals: Set[int]
    searched: List[Point]
    resolved: bool = False


def rho_evaluate(backdoor: Backdoor) -> Point:
    cache = get_process_state().cache

    key = str(backdoor)
    point = cache.get(key)
    if point is not None:
        return point

    point = rho_fn(backdoor)
    cache[key] = point
    return point


def run_alg(
        size: int, seed: int,
        units: List[int],
        iter_count: int
) -> SearchResult:
    pr_state = get_process_state()
    rs_state = RandomState(seed=seed)
    mo_seed = rs_state.randint(2 ** 31)
    so_seed = rs_state.randint(2 ** 31)

    algorithm = MuPlusLambda(
        MU_SIZE, LAMBDA_SIZE,
        selection=Roulette(so_seed),
        mutation=FixSize(size, mo_seed)
    )

    points, literals = {}, set()
    clauses = [[x] for x in units]

    pr_state.rm_literals(units)
    pr_state.add_clauses(clauses)

    while iter_count > 0:
        initial = pr_state.get_initial(
            size, rs_state
        )

        point = rho_evaluate(initial)
        key = str(point.searchable)
        bkv = point.get('value')
        points[key] = point

        with algorithm.start(point) as pm:
            for iteration in range(iter_count):
                backdoor = pm.collect(0, 1)[0]
                point = rho_evaluate(backdoor)

                if point.get('hard') == 0:
                    return SearchResult(
                        set(), [point], True
                    )

                if point.get('hard') == 1:
                    _literals = point.get('first_task')
                    clauses = [[x] for x in _literals]

                    literals.update(set(_literals))
                    pr_state.rm_literals(_literals)
                    pr_state.add_clauses(clauses)
                    points.clear()
                    break

                iter_count -= 1
                _, population = pm.insert(point)
                for point in population:
                    _value = point.get('value')
                    _key = str(point.searchable)
                    if _value == bkv:
                        if _key not in points:
                            points[_key] = point
                    elif _value < bkv:
                        points = {_key: point}
                        bkv = _value

    return SearchResult(literals, [
        rho_fn_ext(point.searchable)
        for point in points.values()
        if point.value() < 1 - MIN_RHO
    ])
    # ] if bkv < 1 - MIN_RHO else [])


def solve(
        runs: int,
        budget: TaskBudget,
        problem: Problem,
        measure: Measure,
        log_path: OptWorkPath,
        bd_size: int = 10,
        iter_count: int = 3000,
        seed_offset: int = 1,
        max_workers: int = 16,

) -> Report:
    dirs = ('examples', 'logs', 'rho_solve')
    log_path = log_path or WorkPath(*dirs)

    with CombineLogger(log_path) as logger:
        workers = min(cpu_count(), max_workers)
        printc(f'Running on {workers} threads')
        executor = init_process_pool(problem, workers)

        printc('', 'Phase 1 (Prepare backdoors)')
        all_points, all_units, tqdm_kwargs = [], set(), {
            'unit': 'run', 'postfix': '0 bds, 0 units',
            'desc': 'Searching', 'total': runs
        }

        seed, futures = runs, []
        with tqdm(**tqdm_kwargs) as progress:
            while seed > 0 or len(futures) > 0:
                while seed > 0 and len(futures) < workers:
                    future = executor.submit(run_alg, *(
                        bd_size, seed_offset + seed,
                        list(all_units), iter_count
                    ))
                    futures.append(future)
                    seed -= 1

                fs = wait(futures, return_when=FIRST_COMPLETED)
                for result in [f.result() for f in fs.done]:
                    literals, searched, _ = result
                    all_points.extend(searched)
                    all_units.update(literals)
                    progress.set_postfix_str(
                        f'{len(all_points)} bds, '
                        f'{len(all_units)} units'
                    )
                    progress.update()

                futures = list(fs.not_done)
            logger.meta(problem, *all_points)

        search_stamp, search_time = time_ms(), passed()
        if len(all_units) != len(set(map(abs, all_units))):
            print(f'Complementary literals was found!')
            return Report(False, {'time': search_time}, None)

        patch, hard_order = rho_preprocess(all_units, all_points, executor)
        pre_stamp, derive_time = time_ms(), passed(search_stamp)
        printc(f'Prepared {len(hard_order)} backdoors')

        phase_1_time = search_time + derive_time
        # todo: reset executor!!!

        printc('', 'Phase 2 (Solve problem)')
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
