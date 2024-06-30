from os import cpu_count
from numpy.random import RandomState

from core.impl import CombineT
from function.module.measure import Measure

from lib_metalg.condition import IterCond
from lib_metalg.algorithm import MuPlusLambda
from lib_metalg.operator.mutation import FixSize
from lib_metalg.ocean import Migration, PointCollector, Ocean
from lib_metalg.operator.selection import Roulette, BestPoint
from lib_metalg.function.process.function_rho import FunctionRho

from lib_satprob.variables import Range
from output.impl import CombineLogger
from space.impl import BackdoorSet

from lib_satprob.solver import Report
from lib_satprob.problem import Problem

from function.module.budget import TaskBudget

from rho_tool.rho_pool import init_process_pool
from rho_tool.rho_order import rho_preprocess

from utility.polyfill import tqdm
from utility.work_path import WorkPath
from utility.format import printc, passed, time_ms

MU_SIZE = 1
LAMBDA_SIZE = 2


def solve(
        problem: Problem,
        bd_count: int,
        group_count: int,
        measure: Measure,
        budget: TaskBudget,
        bd_size: int = 10,
        max_workers: int = 16,
        random_seed: int = 1234,
        log_path: WorkPath = None,
        restart_iter: int = 3000,
        max_value: float = 0.1
) -> Report:
    dirs = ('examples', 'logs', 'rho_solve')
    log_path = log_path or WorkPath(*dirs)
    workers = min(cpu_count(), max_workers)
    state = RandomState(seed=random_seed)

    islands = []
    for i in range(workers):
        mo_seed = state.randint(2 ** 31)
        so_seed = state.randint(2 ** 31)

        algorithm = MuPlusLambda(
            mu_size=MU_SIZE,
            lambda_size=LAMBDA_SIZE,
            selection=Roulette(so_seed),
            mutation=FixSize(bd_size, mo_seed),
            restart_cond=IterCond(restart_iter)
        )
        islands.append(algorithm)

    formula = problem.encoding.get_formula()
    function = FunctionRho(
        max_workers=workers,
        problem=problem
    )
    space = BackdoorSet(
        of_size=bd_size,
        variables=Range(length=formula.nv),
        random_seed=state.randint(2 ** 31),
    )
    # ring
    topology = [
        Migration(
            islands[i],
            islands[i + 1 // len(islands)],
            BestPoint(1), IterCond(100)
        ) for i in range(len(islands))
    ]

    printc(f'Running with {workers} islands')
    printc('', 'Phase 1 (Prepare backdoors)')
    all_points, tqdm_kwargs = [], {
        'unit': 'bd', 'postfix': '0 units',
        'desc': 'Searching', 'total': bd_count
    }
    with tqdm(**tqdm_kwargs) as progress:
        def update_progress(n):
            progress.update(n)

        collector = PointCollector(
            capacity=bd_count,
            diversity=group_count,
            max_value=max_value,
            callback=update_progress
        )
        ocean = Ocean(
            islands=islands,
            function=function,
            topology=topology,
            collector=collector
        )

        points = ocean.launch(space)
        all_points = sorted(list(points))

    executor = init_process_pool(problem, workers)
    search_stamp, search_time = time_ms(), passed()
    patch, hard_order = rho_preprocess(set(), all_points, executor)
    pre_stamp, derive_time = time_ms(), passed(search_stamp)
    printc(f'Prepared {len(hard_order)} backdoors')

    phase_1_time = search_time + derive_time

    with CombineLogger(log_path) as logger:
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
