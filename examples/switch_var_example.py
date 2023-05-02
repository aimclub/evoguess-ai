from numpy.random import RandomState

from core.abc import Estimate
from core.module.space import SearchSet
from core.module.sampling import Const
from core.module.comparator import MinValueMaxSize

from function.impl import GuessAndDetermine
from function.module.solver import pysat
from function.module.measure import SolvingTime
# from function.module.measure import Propagations, Conflicts, LearnedLiterals

from instance import Instance
from instance.module.encoding import CNF
from instance.module.variables import Variables
from instance.module.variables.vars import XorSwitch, compress
# from instance.module.variables.vars import Switch, Bent4Switch, MajoritySwitch

from util.iterable import slice_by
from typings.work_path import WorkPath
from executor.impl import ProcessExecutor

if __name__ == '__main__':
    # XorSwitch(
    #       name - uniq var name,
    #       group - list of var indexes
    # )
    variables = Variables(from_vars=[
        XorSwitch('x1', [43, 44]),  # for example: group=[43, 44] -> x1 = v43 ^ v44)
        XorSwitch('x2', [45, 81]), XorSwitch('x3', [82, 83]), XorSwitch('x4', [84, 85])
    ])
    # predefined Switches: XorSwitch, Bent4Switch, MajoritySwitch

    # or use custom function in Switch
    # Switch(
    #       name - uniq var name,
    #       group - list of var indexes
    #       fn - boolean function
    # )
    #
    # def my_xor(x1, x2) -> bool:
    #     return bool(x1 ^ x2)
    #
    # variables = Variables(from_vars=[
    #     Switch('x1', [43, 44], my_xor), Switch('x2', [45, 81], my_xor),
    #     Switch('x3', [82, 83], my_xor), Switch('x4', [84, 85], my_xor)
    # ])

    # generate supplements (Assumptions, Constraints) from var values (
    var_map = {43: 1, 44: 0, 45: 0, 81: 0, 82: 1, 83: 1, 84: 1, 85: 0}
    supplements = compress(*(var.supplements(var_map) for var in variables))
    # ([], [[43, 44], [-43, -44], [45, -81], [-45, 81], [82, -83], [-82, 83], [84, 85], [-84, -85]])

    # generate supplements (Assumptions, Constraints) from Switch var values
    # var_map = {'x1': 0, 'x2': 1, 'x3': 1, 'x4': 0}
    # supplements = compress(*(var.supplements(var_map) for var in variables))
    # ([], [[43, -44], [-43, 44], [45, 81], [-45, -81], [82, 83], [-82, -83], [84, -85], [-84, 85]])

    # generate list of random supplements
    state = RandomState(seed=47283)
    var_bases = variables.get_var_bases()  # bases for all var in variables (base=2 for switch vars)
    substitutions = state.randint(0, var_bases, (5, len(var_bases)))
    for substitution in substitutions:
        var_map = {var: value for var, value in zip(variables, substitution)}
        supplements = compress(*(var.supplements(var_map) for var in variables))
    # ([], [[43, -44], [-43, 44], [45, -81], [-45, 81], [82, -83], [-82, 83], [84, -85], [-84, 85]])
    # ([], [[43, 44], [-43, -44], [45, 81], [-45, -81], [82, -83], [-82, 83], [84, 85], [-84, -85]])
    # ([], [[43, 44], [-43, -44], [45, 81], [-45, -81], [82, 83], [-82, -83], [84, -85], [-84, 85]])
    # ([], [[43, 44], [-43, -44], [45, -81], [-45, 81], [82, 83], [-82, -83], [84, 85], [-84, -85]])
    # ([], [[43, -44], [-43, 44], [45, -81], [-45, 81], [82, -83], [-82, 83], [84, 85], [-84, -85]])

    #
    # estimate fitness value for sgen_150 encoding
    # with backdoor of switch variables: x1..x20
    # x1 = v1 ^ v2, x2 = v3 ^ v4, ...
    #
    data_path = WorkPath('examples', 'data', root='..')
    sgen_path = data_path.to_file('sgen_150.cnf')
    space = SearchSet(variables=Variables(from_vars=[
        XorSwitch(f'x{i + 1}', list(group)) for i, group
        in enumerate(slice_by(range(1, 41), 2))
    ]))
    function = GuessAndDetermine(
        solver=pysat.Glucose3(),
        measure=SolvingTime(),
    )
    instance = Instance(
        encoding=CNF(from_file=sgen_path)
    )

    estimator = Estimate(
        logger=None,
        space=space,
        instance=instance,
        function=function,
        sampling=Const(size=2 ** 14, split_into=1024),
        executor=ProcessExecutor(max_workers=4),
        comparator=MinValueMaxSize(),
    )

    backdoor = space.get_initial(instance)
    handle = estimator.estimate(backdoor)  # async object
    point = handle.result()  # await result
    print('vars: ', point.backdoor)
    print('fitness value: ', point.value())
    # if backdoor.power == sampling.size then
    # fitness value is estimated over all possible substitutions
    # else
    # fitness value is estimated over random set of substitutions
