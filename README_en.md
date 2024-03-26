[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)

[![license](https://img.shields.io/github/license/aimclub/evoguess-ai)](https://github.com/aimclub/evoguess-ai/blob/master/LICENSE)
[![Eng](https://img.shields.io/badge/lang-ru-yellow.svg)](/README.md)
[![Mirror](https://img.shields.io/badge/mirror-GitLab-orange)](https://gitlab.actcognitive.org/itmo-sai-code/evoguess-ai)

# EvoGuessAI

Component for finding decomposition sets and estimating hardness of SAT instances. The search for decomposition sets is realized via the optimization of the special pseudo-Boolean black-box functions that estimate the hardness of the decomposition corresponding to the employed decomposition method and the considered set. To optimize the value of such functions the component uses metaheuristic algorithms, in particular, the evolutionary ones.

## Installation

```shell script
git clone git@github.com:ctlab/evoguess-ai.git
cd evoguess-ai
pip install -r requirements.txt
```
To use EvoGuessAI in MPI mode, you also need to install:

```shell script
pip install -r requirements-mpi.txt
```

### How to MPI use

The EvoGuessAI can be run in MPI mode as follows:

```shell script
mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main.py
```

where **perhost** is MPI workers processes on one node, and **workers** is a total MPI workers processes on all dedicated nodes.

## Rho-backdoors

EvoGuessAI supports the use of rho-backdoors to solve SAT and MaxSAT in relation to СNF.

Rho-backdoor, in short, is a backdoor that allows you to decompose the original CNF into two subsets of subtasks. The first will consist of subtasks that the SAT oracle solves for a certain limitation by some measure (most often, time or number of conflicts), the second of all other subtasks. The proportion of the first subset is (rho), the second is (1-rho).

In practice (and in EvoGuessAI), such backdoors are sought to maximize rho. Accordingly, each backdoor will generate a small number of complex subtasks (also called _hardtasks_). However, we can use the hardtasks received from different backdoors together.

EvoGuessAI is able to build backdoors while maximizing the rho value. Then the iterative process of filtering out hardtasks is started. At each iteration, the Cartesian product of hardtacks from different rho backdoors is built and then it is filtered to find new hardtacks. At some point, all the hard tasks begin to be solved for the set limit to some extent. If the rho backdoors for building Cartesian products end earlier, then the restriction is disabled and all remaining tasks are completed as usual.

### Requirements

Optional:
1. tqdm – package for logging the process.
```shell
pip install tqdm
```

[//]: # (Требуемые пакеты, опциональные и обязательные, и тд)

[//]: # ()
[//]: # (&#40;заглушка для tqdm надо доделать, желательно&#41;)

### Rho-backdoors mode command line parameters

| Argument        | Short name | Description                                                                                                                                                                                                                               |
|-----------------|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --formula       | -f         | file with cnf, is a required parameter                                                                                                                                                                                                    |
| --solvername    | -s         | short name of the SAT solver used as the SAT oracle. Available names: g3 -- Glucose 3; cd, cd 15, cd19 -- different versions of Cadical (see PySAT docs);                                                                                 |
| --nofearuns     | -nr        | the number of runs of the evolutionary algorithm for searching for rho backdoors. Each launch can result in the generation of several rho backdoors if they have the same rho;                                                            |
| --seedinitea    | -seed      | initializing seed for the evolutionary algorithm;                                                                                                                                                                                         |
| --nofprocesses  | -np        | the number of available processes for multithreading;                                                                                                                                                                                     |
| --backdoorsize  | -bds       | the size of the rho backdoors being searched;                                                                                                                                                                                             |
| --timelimit     | -tl        | time limit for the SAT oracle when solving hard tasks;                                                                                                                                                                                    |
| --conflictlimit | -cl        | limit on the number of conflicts for the SAT oracle when solving hardtacks. At startup, only one of the options for restrictions is selected (the maximum set), respectively, either a time limit or a number of conflicts should be set. |

[//]: # (Надо посомтреть форматы записи параметров и сделать по-красоте)

[//]: # ()
[//]: # (Стоит добавить функционал для SAT-задач.)

[//]: # ()
[//]: # (Можно добавить &#40;в документции&#41; доп параметры для advanced использования, которые будут уже не в командной строке, а внутри main_p. К примеру параметр перезапуска екзекьютора)

Default run:
```shell
python3 ./main_p.py -cnf ./examples/data/lec_sort_PvS_8_3.cnf -s g3 -nr 40 -seed 123 -np 8 -bds 10 -tl 0 -cl 20000
```
This command will launch EvoGuessAI in the mode of using rho backdoors to solve one of the exemplary CNF (LEC problem for the "pancake" and "selection" sorting algorithms for eight 3-bit numbers). 8 processes will be used in the solution. The evolutionary algorithm will be run 40 times with a "123" seed, while looking for rho backdoors of length 10. Hardtacks will be solved with a limit of 20,000 conflicts per hardtask.

[//]: # (Нужен эффективный пример)

[//]: # (Показать примеры работы прям тут с пояснениями и все такое)

[//]: # ()
[//]: # (Нужно добавить функционал, чтобы если у нас бэкдор с одной хардтаской, то сразу добавляем юниты к кнф через солвер.екстенд)

[//]: # (и бэкдор тогда не доабвляем)

[//]: # ()
[//]: # (И вообще все сложнее, потому что эти переменные могут быть в бэкдорах, найденных до этого. И ещё из пространтсва поиска надо удалять юниты. А для этого надо чтобы в принципе пространство поиска динамически менялось)

[//]: # ()
[//]: # (solver._solver.add_clause&#40;[l for l in hardtask]&#41; &#40;только надо ещё проверить что _solver существует&#41;)

[//]: # ()
[//]: # (Ещё хорошая идея после поиска бэкдоров убивать все солверы и потом их пересоздавать, чтобы чистился кэш)

## Usage examples

An example of [probabilistic backdoors searching](https://github.com/aimclub/evoguess-ai/blob/master/examples/pvs_search_example.py) to solve the equivalence checking problem of two Boolean schemes that implement different algorithms, using the example of PvS 7x4 encoding (Pancake vs Selection sort).

```python
root_path = WorkPath('examples')
data_path = root_path.to_path('data')
cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
logs_path = root_path.to_path('logs', 'pvs_4_7')

problem = SatProblem(
    encoding=CNF(from_file=cnf_file),
    solver=PySatSolver(sat_name='g3'),
)
solution = Optimize(
    problem=problem,
    space=BackdoorSet(
        by_vector=[],
        variables=rho_subset(
            problem,
            Range(start=1, length=1213),
            of_size=200
        )
    ),
    executor=ProcessExecutor(max_workers=16),
    sampling=Const(size=8192, split_into=2048),
    function=RhoFunction(
        penalty_power=2 ** 20,
        measure=Propagations(),
    ),
    algorithm=Elitism(
        elites_count=2,
        population_size=6,
        mutation=Doer(),
        crossover=TwoPoint(),
        selection=Roulette(),
        min_update_size=6
    ),
    limitation=WallTime(from_string='02:00:00'),
    comparator=MinValueMaxSize(),
    logger=OptimizeLogger(logs_path),
).launch()
```

Further, the corresponding problem of checking the equivalence of two Boolean schemes using the example of PvS 7x4 encoding can be [solved using the found backdoors](https://github.com/aimclub/evoguess-ai/blob/master/examples/pvs_solve_example.py) as follows:

```python
root_path = WorkPath('examples')
data_path = root_path.to_path('data')
cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
logs_path = root_path.to_path('logs', 'pvs_4_7_comb')
estimation = Combine(
    problem=SatProblem(
        encoding=CNF(from_file=cnf_file),
        solver=PySatSolver(sat_name='g3'),
    ),
    logger=OptimizeLogger(logs_path),
    executor=ProcessExecutor(max_workers=16)
).launch(*backdoors)
```

Other [examples](https://github.com/aimclub/evoguess-ai/tree/master/examples) can be found in the corresponding project directory.

## Supported by

The study is supported by the [Research Center Strong Artificial Intelligence in Industry](<https://sai.itmo.ru/>) 
of [ITMO University](https://en.itmo.ru/) as part of the plan of the center's program: Development and testing of an experimental prototype of a library of strong AI algorithms in terms of the Boolean satisfiability problem solving through heuristics of working with constraints and variables, searching for probabilistic trapdoors and inverse polynomial trapdoors.

## Documentation

Documentation is available [here](https://evoguess-ai.readthedocs.io/) and includes installation instructions and base usage manual.
