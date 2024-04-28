[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)

[![license](https://img.shields.io/github/license/aimclub/evoguess-ai)](https://github.com/aimclub/evoguess-ai/blob/master/LICENSE)
[![Eng](https://img.shields.io/badge/lang-ru-yellow.svg)](/README.md)
[![Mirror](https://img.shields.io/badge/mirror-GitLab-orange)](https://gitlab.actcognitive.org/itmo-sai-code/evoguess-ai)

# EvoGuessAI

A component for finding decomposition sets and using them to solve SAT instances. 
The search for decomposition sets is performed by optimising special 
pseudo-boolean black-box functions that evaluate either the ρ-value 
in the case of using EvoguessAI in ρ-backdoors mode, or the decomposition 
hardness corresponding to the decomposition method used 
and the set under consideration in the case of IBS mode. 
The component uses metaheuristic algorithms, in particular 
evolutionary algorithms, to optimise the values of such functions.


## Installation

```shell script
git clone git@github.com:ctlab/evoguess-ai.git
cd evoguess-ai
pip install -r requirements.txt
```

[//]: # (To use EvoGuessAI in MPI mode, you also need to install:)

[//]: # ()
[//]: # (```shell script)

[//]: # (pip install -r requirements-mpi.txt)

[//]: # (```)

### Dependences

Requirement packages:
1. [numpy](https://numpy.org/) (>=1.21.6)
   > pip install numpy

2. [python-sat](https://pysathq.github.io/) (~=1.8.dev4) – PySAT is a toolkit 
that provides convenient functionality for using SAT oracles. 
   > pip install python-sat

Optional packages:
1. [tqdm](https://tqdm.github.io/) – package for logging the process.
   > pip install tqdm

## ρ-Backdoors mode

EvoGuessAI supports the use of ρ-backdoors to solve SAT in relation to 
СNF and MaxSAT in relation to WCNF.

ρ-Backdoor, in short, is a backdoor that allows you to decompose 
the original CNF into two subsets of subtasks. The first will consist of 
subtasks that the SAT oracle solves for a certain limitation 
by some measure (most often, time or number of conflicts), 
the second of all other subtasks. 
The proportion of the first subset is (ρ), the second is (1-ρ).

In practice (and in EvoGuessAI), such backdoors are sought to maximize ρ. 
Accordingly, each backdoor will generate a small number of complex 
subtasks (also called _hard tasks_). However, we can use the hard tasks 
received from different backdoors together.

EvoGuessAI is able to build backdoors while maximizing the ρ value. 
Then the iterative process of filtering out hard tasks is started. 
At each iteration, the Cartesian product of hard tasks from different 
ρ-backdoors is built and then it is filtered to find new hard tasks. 
At some point, all the hard tasks begin to be solved for 
some limit (in time or conflicts). If the ρ-backdoors for 
building Cartesian products end earlier, then the limit 
is disabled and all remaining tasks are completed as usual.


### Usage

```
python3 main_rho.py [-h] 
                    [-s [SOLVERNAME]] [-nr [NOFEARUNS]] 
                    [-np [NOFPROCESSES]] [-bds [BACKDOORSIZE]] 
                    [-tl [TIMELIMIT]] [-cl [CONFLICTLIMIT]]
                    formula
```


### ρ-Backdoor's module command line parameters

| Argument full name | Short name | Description                                                                                                                                                                                                                               |
|------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| formula          |         | file with input formula (CNF or WCNF format), is a positional parameter                                                                                                                                                                   |
| --solvername     | -s      | short name of the SAT solver used as the SAT oracle. Available names: g3 -- Glucose 3; cd, cd 15, cd19 -- different versions of Cadical (see PySAT docs)                                                                                  |
| --nofearuns      | -nr     | the number of runs of the evolutionary algorithm for searching for ρ-backdoors. Each launch can result in the generation of several ρ-backdoors if they have the same ρ                                                                   |
| --nofprocesses   | -np     | the number of available processes for multithreading                                                                                                                                                                                      |
| --backdoorsize   | -bds    | the size of the ρ-backdoors being searched                                                                                                                                                                                                |
| --timelimit      | -tl     | time limit for the SAT oracle when solving hard tasks                                                                                                                                                                                     |
| --conflictlimit  | -cl     | limit on the number of conflicts for the SAT oracle when solving hard tasks. At startup, only one of the options for restrictions is selected (the maximum set), respectively, either a time limit or a number of conflicts should be set |

[//]: # (Мб стоит сид убать в адвансед параметры, всетаки это не особо "осознанный" параметр в плане изменения)

[//]: # (Надо посомтреть форматы записи параметров и сделать по-красоте)

[//]: # ()
[//]: # (Стоит добавить функционал для SAT-задач.)

[//]: # ()
[//]: # (Можно добавить &#40;в документции&#41; доп параметры для advanced использования, которые будут уже не в командной строке, а внутри main_p. К примеру параметр перезапуска екзекьютора)


Example:
```shell
python3 ./main_rho.py -f ./examples/data/lec_sort_PvS_8_3.cnf -s g3 -nr 40 -np 8 -bds 10 -tl 0 -cl 20000
```
Command above will launch EvoGuessAI in the mode of using 
ρ-backdoors to solve one of the exemplary CNF 
(LEC problem for the "pancake" and "selection" sorting 
algorithms for eight 3-bit numbers). 8 processes will be used 
in the solution. The evolutionary algorithm will be run 40 
times, while looking for ρ-backdoors of length 10. Hard tasks 
will be solved with a limit of 20,000 conflicts per task.

Result with comments:

[//]: # (TODO нужен нормальный пример)
```shell
00:00:01 ---------------------- Running on 4 threads ----------------------
00:00:01 -------------------------------------------------------------------
00:00:01 ------------------- Phase 1 (Prepare backdoors) -------------------
00:00:01 Searching: 100%|██████████| 40/40 [03:31<00:00,  5.29s/run, 7009 bds]

# In phase 1 7009 backdoors was found. It was backdoors with maximum rho from every thread.

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
# When solving these 4 cubes with a limit in conflicts, it turned out that all 4 were too difficult. 
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

# Since backdoor 10 was the last one, remain hard tasks is solved without limit.

00:25:51 Sifting: 100%|██████████| 788/788 [46:31<00:00,  3.54s/task, 0 hard]
01:12:23 -------------------------------------------------------------------
01:12:23 ---------------------------- Solution ----------------------------
01:12:23 -------------------------- UNSATISFIABLE --------------------------

# EvoguessAI proved that formula is unsatisfiable.

01:12:23 -------------------------------------------------------------------
01:12:23 -------------------- Search time: 213.179 sec. --------------------
01:12:23 -------------------- Derive time: 52.396 sec. --------------------
01:12:23 ------------------- Solving time: 4077.635 sec. -------------------
01:12:23 -------------------------------------------------------------------
01:12:23 ------------------- Summary time: 4343.21 sec. -------------------
```


[//]: # (## IBS mode)


[//]: # (### How to MPI use)

[//]: # ()
[//]: # (The EvoGuessAI can be run in MPI mode as follows:)

[//]: # ()
[//]: # (```shell script)

[//]: # (mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main.py)

[//]: # (```)

[//]: # ()
[//]: # (where **perhost** is MPI workers processes on one node, )

[//]: # (and **workers** is a total MPI workers processes on all dedicated nodes.)


[//]: # (## Usage examples)

[//]: # ()
[//]: # (An example of [probabilistic backdoors searching]&#40;https://github.com/aimclub/evoguess-ai/blob/master/examples/pvs_search_example.py&#41; to solve the equivalence checking problem of two Boolean schemes that implement different algorithms, using the example of PvS 7x4 encoding &#40;Pancake vs Selection sort&#41;.)

[//]: # ()
[//]: # (```python)

[//]: # (root_path = WorkPath&#40;'examples'&#41;)

[//]: # (data_path = root_path.to_path&#40;'data'&#41;)

[//]: # (cnf_file = data_path.to_file&#40;'pvs_4_7.cnf', 'sort'&#41;)

[//]: # (logs_path = root_path.to_path&#40;'logs', 'pvs_4_7'&#41;)

[//]: # ()
[//]: # (problem = SatProblem&#40;)

[//]: # (    encoding=CNF&#40;from_file=cnf_file&#41;,)

[//]: # (    solver=PySatSolver&#40;sat_name='g3'&#41;,)

[//]: # (&#41;)

[//]: # (solution = Optimize&#40;)

[//]: # (    problem=problem,)

[//]: # (    space=BackdoorSet&#40;)

[//]: # (        by_vector=[],)

[//]: # (        variables=rho_subset&#40;)

[//]: # (            problem,)

[//]: # (            Range&#40;start=1, length=1213&#41;,)

[//]: # (            of_size=200)

[//]: # (        &#41;)

[//]: # (    &#41;,)

[//]: # (    executor=ProcessExecutor&#40;max_workers=16&#41;,)

[//]: # (    sampling=Const&#40;size=8192, split_into=2048&#41;,)

[//]: # (    function=RhoFunction&#40;)

[//]: # (        penalty_power=2 ** 20,)

[//]: # (        measure=Propagations&#40;&#41;,)

[//]: # (    &#41;,)

[//]: # (    algorithm=Elitism&#40;)

[//]: # (        elites_count=2,)

[//]: # (        population_size=6,)

[//]: # (        mutation=Doer&#40;&#41;,)

[//]: # (        crossover=TwoPoint&#40;&#41;,)

[//]: # (        selection=Roulette&#40;&#41;,)

[//]: # (        min_update_size=6)

[//]: # (    &#41;,)

[//]: # (    limitation=WallTime&#40;from_string='02:00:00'&#41;,)

[//]: # (    comparator=MinValueMaxSize&#40;&#41;,)

[//]: # (    logger=OptimizeLogger&#40;logs_path&#41;,)

[//]: # (&#41;.launch&#40;&#41;)

[//]: # (```)

[//]: # ()
[//]: # (Further, the corresponding problem of checking the equivalence of two Boolean schemes using the example of PvS 7x4 encoding can be [solved using the found backdoors]&#40;https://github.com/aimclub/evoguess-ai/blob/master/examples/pvs_solve_example.py&#41; as follows:)

[//]: # ()
[//]: # (```python)

[//]: # (root_path = WorkPath&#40;'examples'&#41;)

[//]: # (data_path = root_path.to_path&#40;'data'&#41;)

[//]: # (cnf_file = data_path.to_file&#40;'pvs_4_7.cnf', 'sort'&#41;)

[//]: # (logs_path = root_path.to_path&#40;'logs', 'pvs_4_7_comb'&#41;)

[//]: # (estimation = Combine&#40;)

[//]: # (    problem=SatProblem&#40;)

[//]: # (        encoding=CNF&#40;from_file=cnf_file&#41;,)

[//]: # (        solver=PySatSolver&#40;sat_name='g3'&#41;,)

[//]: # (    &#41;,)

[//]: # (    logger=OptimizeLogger&#40;logs_path&#41;,)

[//]: # (    executor=ProcessExecutor&#40;max_workers=16&#41;)

[//]: # (&#41;.launch&#40;*backdoors&#41;)

[//]: # (```)

[//]: # ()
[//]: # (Other [examples]&#40;https://github.com/aimclub/evoguess-ai/tree/master/examples&#41; can be found in the corresponding project directory.)

## Supported by

The study is supported by the [Research Center Strong Artificial Intelligence in Industry](<https://sai.itmo.ru/>) 
of [ITMO University](https://en.itmo.ru/) as part of the plan of the center's program: Development and testing of an experimental prototype of a library of strong AI algorithms in terms of the Boolean satisfiability problem solving through heuristics of working with constraints and variables, searching for probabilistic trapdoors and inverse polynomial trapdoors.

## Documentation

Documentation for the main modes of the EvoguessAI usage is available 
in the [Markdown](https://en.wikipedia.org/wiki/Markdown) file [`intro.md`](rho_docs_en/intro.md).

## Low-level usage

Also EvoguessAI supports its use at low level and as a library. 
In this mode the user can use his own implementations of classes and functions. 
Documentation for this mode is available
[here](https://evoguess-ai.readthedocs.io/) and includes installation 
instructions and base usage manual.
