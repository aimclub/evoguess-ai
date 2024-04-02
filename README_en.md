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

## ρ-Backdoors module

EvoGuessAI supports the use of ρ-backdoors to solve SAT in relation to СNF and MaxSAT in relation to WCNF.

ρ-Backdoor, in short, is a backdoor that allows you to decompose the original CNF into two subsets of subtasks. The first will consist of subtasks that the SAT oracle solves for a certain limitation by some measure (most often, time or number of conflicts), the second of all other subtasks. The proportion of the first subset is (ρ), the second is (1-ρ).

In practice (and in EvoGuessAI), such backdoors are sought to maximize ρ. Accordingly, each backdoor will generate a small number of complex subtasks (also called _hard tasks_). However, we can use the hard tasks received from different backdoors together.

EvoGuessAI is able to build backdoors while maximizing the ρ value. Then the iterative process of filtering out hard tasks is started. At each iteration, the Cartesian product of hard tasks from different ρ-backdoors is built and then it is filtered to find new hard tasks. At some point, all the hard tasks begin to be solved for the set limit to some extent. If the ρ-backdoors for building Cartesian products end earlier, then the restriction is disabled and all remaining tasks are completed as usual.

### Requirements

Optional:
1. tqdm – package for logging the process.
```shell
pip install tqdm
```

[//]: # (Требуемые пакеты, опциональные и обязательные, и тд)

[//]: # ()
[//]: # (&#40;заглушка для tqdm надо доделать, желательно&#41;)

### ρ-Backdoor's module documentation

In the [Markdown](https://en.wikipedia.org/wiki/Markdown) file
[`index.md`](rho_docs_en/index.md).

### ρ-Backdoor's module command line parameters

| Argument full name | Short name | Description                                                                                                                                                                                                                               |
|--------------------|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --formula          | -f         | file with input formula (CNF or WCNF format), is a required parameter                                                                                                                                                                     |
| --solvername       | -s         | short name of the SAT solver used as the SAT oracle. Available names: g3 -- Glucose 3; cd, cd 15, cd19 -- different versions of Cadical (see PySAT docs)                                                                                  |
| --nofearuns        | -nr        | the number of runs of the evolutionary algorithm for searching for ρ-backdoors. Each launch can result in the generation of several ρ-backdoors if they have the same ρ                                                                   |
| --nofprocesses     | -np        | the number of available processes for multithreading                                                                                                                                                                                      |
| --backdoorsize     | -bds       | the size of the ρ-backdoors being searched                                                                                                                                                                                                |
| --timelimit        | -tl        | time limit for the SAT oracle when solving hard tasks                                                                                                                                                                                     |
| --conflictlimit    | -cl        | limit on the number of conflicts for the SAT oracle when solving hard tasks. At startup, only one of the options for restrictions is selected (the maximum set), respectively, either a time limit or a number of conflicts should be set |

[//]: # (Мб стоит сид убать в адвансед параметры, всетаки это не особо "осознанный" параметр в плане изменения)

[//]: # (Надо посомтреть форматы записи параметров и сделать по-красоте)

[//]: # ()
[//]: # (Стоит добавить функционал для SAT-задач.)

[//]: # ()
[//]: # (Можно добавить &#40;в документции&#41; доп параметры для advanced использования, которые будут уже не в командной строке, а внутри main_p. К примеру параметр перезапуска екзекьютора)

Template:
```shell
python3 ./main_p.py -f <file> [options]
```
Example:
```shell
python3 ./main_p.py -f ./examples/data/lec_sort_PvS_8_3.cnf -s g3 -nr 40 -np 8 -bds 10 -tl 0 -cl 20000
```
Command above will launch EvoGuessAI in the mode of using ρ-backdoors to solve one of the exemplary CNF (LEC problem for the "pancake" and "selection" sorting algorithms for eight 3-bit numbers). 8 processes will be used in the solution. The evolutionary algorithm will be run 40 times, while looking for ρ-backdoors of length 10. Hard tasks will be solved with a limit of 20,000 conflicts per hard task.

Result with comments:

[//]: # (сделать такой формат примера, чтобы комментарии выделялись визуально)
```shell
00:00:01 ---------------------- Running on 4 threads ----------------------
00:00:01 -------------------------------------------------------------------
00:00:01 ------------------- Phase 1 (Prepare backdoors) -------------------
00:00:01 Searching: 100%|██████████| 40/40 [03:31<00:00,  5.29s/run, 7009 bds]

# In phase 1 7009 backdoors was found. It was bacdoors with maximum rho from every thread

00:03:33 Deriving: 100%|██████████| 608/608 [00:52<00:00, 11.65bd/s, 844 clauses]

# During deriving process from all backdoor 844 additional clauses was extract to the original CNF.

00:04:25 ---------------------- Prepared 10 backdoors ----------------------

# All backdoors were filtered from useless ones (not carrying new variables). 
# 10 backdoors left.

00:04:25 -------------------------------------------------------------------
00:04:25 --------------------- Phase 2 (Solve problem) ---------------------
00:04:25 ------------------- Used 2 backdoors (20 vars) -------------------
00:04:25 Sifting: 100%|██████████| 4/4 [00:04<00:00,  1.06s/task, 4 hard]

# Hard tasks from first two backdoor was used to construct Cortesian product. It's lenght is 4 cubes.
# When solving these 4 cubes with a constraint, it turned out that all 4 were too difficult. 
# Therefore, we add the next backdoor (builds the Cartesian product of the current set of cubes 
# and the hard tasks from the next backdoor).

00:04:29 ------------------- Used 3 backdoors (22 vars) -------------------
00:04:29 Sifting: 100%|██████████| 8/8 [00:07<00:00,  1.14task/s, 8 hard]
00:04:36 ------------------- Used 4 backdoors (24 vars) -------------------
00:04:36 Sifting: 100%|██████████| 16/16 [00:15<00:00,  1.03task/s, 16 hard]
00:04:52 ------------------- Used 5 backdoors (26 vars) -------------------
00:04:52 Sifting: 100%|██████████| 32/32 [00:31<00:00,  1.02task/s, 32 hard]
00:05:23 ------------------- Used 6 backdoors (36 vars) -------------------
00:05:23 Sifting: 100%|██████████| 64/64 [01:03<00:00,  1.01task/s, 64 hard]
00:06:27 ------------------- Used 7 backdoors (38 vars) -------------------
00:06:27 Sifting: 100%|██████████| 128/128 [02:22<00:00,  1.11s/task, 125 hard]
00:08:49 ------------------- Used 8 backdoors (39 vars) -------------------
00:08:49 Sifting: 100%|██████████| 250/250 [05:41<00:00,  1.37s/task, 220 hard]
00:14:31 ------------------- Used 9 backdoors (42 vars) -------------------
00:14:31 Sifting: 100%|██████████| 440/440 [11:20<00:00,  1.55s/task, 394 hard]
00:25:51 ------------------- Used 10 backdoors (44 vars) -------------------
00:25:51 -------------- Disable solver budget (last backdoor) --------------
00:25:51 Sifting: 100%|██████████| 788/788 [46:31<00:00,  3.54s/task, 0 hard]
01:12:23 -------------------------------------------------------------------
01:12:23 ---------------------------- Solution ----------------------------
01:12:23 -------------------------- UNSATISFIABLE --------------------------
01:12:23 -------------------------------------------------------------------
01:12:23 -------------------- Search time: 213.179 sec. --------------------
01:12:23 -------------------- Derive time: 52.396 sec. --------------------
01:12:23 ------------------- Solving time: 4077.635 sec. -------------------
01:12:23 -------------------------------------------------------------------
01:12:23 ------------------- Summary time: 4343.21 sec. -------------------

Process finished with exit code 0
```


[//]: # (Нужен эффективный пример)

[//]: # (Показать примеры работы прям тут с пояснениями и все такое)

[//]: # ()
[//]: # (Нужно добавить функционал, чтобы если у нас бэкдор с одной хардтаской, то сразу добавляем юниты к кнф через солвер.екстенд)

[//]: # (и бэкдор тогда не доабвляем)

[//]: # ()
[//]: # (И вообще все сложнее, потому что эти переменные могут быть в бэкдорах, найденных до этого. И ещё из пространтсва поиска надо удалять юниты. А для этого надо чтобы в принципе пространство поиска динамически менялось)

[//]: # ()
[//]: # (solver._solver.add_clause&#40;[l for l in hard task]&#41; &#40;только надо ещё проверить что _solver существует&#41;)

[//]: # ()
[//]: # (Ещё хорошая идея после поиска бэкдоров убивать все солверы и потом их пересоздавать, чтобы чистился кэш)
[//]: # (Ещё нужно сделать, чтобы бэкдоры искались с константным решателем с быстрым пропагейтом, а вот потом уже решение шло на выбранном пользователем решателе)

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
