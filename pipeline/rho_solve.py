from typing import List
from os import cpu_count, getpid
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

from lib_satprob.encoding.patch import SatPatch

MU_SIZE = 1
LAMBDA_SIZE = 1


def rho_evaluate(backdoor: Backdoor) -> Point:
    cache = get_process_state().cache

    key = str(backdoor)
    point = cache.get(key)
    if point is not None:
        return point

    point = rho_fn(backdoor)
    cache[key] = point
    return point


def run_alg(size: int, seed: int, iter_count: int) -> (List[Point], list):
    state = RandomState(seed=seed)
    mo_seed = state.randint(2 ** 31)
    so_seed = state.randint(2 ** 31)

    algorithm = MuPlusLambda(
        MU_SIZE, LAMBDA_SIZE,
        selection=Roulette(so_seed),
        mutation=FixSize(size, mo_seed)
    )

    lits = []
    remain_iters = iter_count
    while True:
        relaunch = False
        space = get_process_state().space
        vector = state.randint(0, 2, size)
        initial = space._get_searchable()
        initial._set_vector(list(vector))

        best_value, point = 1, rho_evaluate(initial)
        same_value = {str(point.searchable): point}
        with algorithm.start(point) as pm:
            for iteration in range(remain_iters):
                backdoor = pm.collect(0, 1)[0]
                point = rho_evaluate(backdoor)

                # if len(point.get('hard')) == 0:
                #   задачу решили

                if point.get('hard') == 1:
                    new_lits = point.get('first_task')
                    # print(f'New lits: {new_lits}')
                    new_lits_patch = SatPatch([[x] for x in new_lits])
                    get_process_state().solver.apply(new_lits_patch)
                    lits.extend(new_lits)

                    new_variables = []
                    for var in backdoor._variables:
                        for y in [abs(k) for k in new_lits]:
                            if var == y: break
                        else:
                            new_variables.append(var)

                    # print(f'old {len(backdoor._variables)}, new {len(new_variables)}')
                    get_process_state().space.variables = new_variables
                    remain_iters = remain_iters - (iteration+1)
                    relaunch = True
                    # print(f'PID: {getpid()}. New lits: {new_lits}. Relaunch. Remain iterations: {remain_iters}')
                    break

                # print(f'PID: {os.getpid()}, iter {iteration} of {range(remain_iters)}, point {point}')
                _, population = pm.insert(point)
                for point in population:
                    _value = point.get('value')
                    _key = str(point.searchable)
                    if _value == best_value:
                        if _key not in same_value:
                            same_value[_key] = point
                    elif _value < best_value:
                        same_value = {_key: point}
                        best_value = _value
            if relaunch == True:
                continue

        return [
            rho_fn_ext(point.searchable)
            for point in same_value.values()
        ], lits


def solve(
        problem: Problem,
        runs: int,
        measure: Measure,
        seed_offset: int = 1,
        max_workers: int = 16,
        bd_size: int = 10,
        limit: int = 20000,
        log_path: WorkPath = None,
        iter_count: int = 3000
) -> Report:
    dirs = ('examples', 'logs', 'rho_solve')
    log_path = log_path or WorkPath(*dirs)
    from lib_satprob.solver import PySatSolver
    prop_solver = PySatSolver('m22')  # const solver for propagate() (not depend on solver "power")
    solve_solver = problem.solver  # user defined solver for solve()
    problem.solver = prop_solver

    with CombineLogger(log_path) as logger:
        workers = min(cpu_count(), max_workers)
        printc(f'Running on {workers} threads')
        executor = init_process_pool(problem, workers)

        printc('', 'Phase 1 (Prepare backdoors)')
        all_points, tqdm_kwargs = [], {
            'unit': 'run', 'postfix': '0 bds, 0 units',
            'desc': 'Searching', 'total': runs
        }
        all_lits = set()
        with tqdm(**tqdm_kwargs) as progress:
            for points, lits in executor.map(run_alg, *zip(*(
                    (bd_size, seed_offset + seed, iter_count)
                    for seed in range(runs)
            ))):
                progress.update()
                all_points.extend(points)
                all_lits.update(set(lits))
                progress.set_postfix_str(
                    f'{len(all_points)} bds, {len(all_lits)} units'
                )
            logger.meta(problem, *all_points)
        # for el in sorted(all_points):
            # print(el)
        if len(all_lits) != len(set(map(abs, all_lits))):
            print(f'Complementary literals was found.')
        search_stamp, search_time = time_ms(), passed()
        patch, hard_order = rho_preprocess(all_points, executor, all_lits)
        pre_stamp, derive_time = time_ms(), passed(search_stamp)
        printc(f'Prepared {len(hard_order)} backdoors')
        # print(hard_order)

        phase_1_time = search_time + derive_time

        printc('', 'Phase 2 (Solve problem)')
        problem.solver = solve_solver
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
