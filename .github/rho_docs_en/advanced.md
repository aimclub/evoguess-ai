# EvoGuessAI
[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)

[![license](https://img.shields.io/github/license/aimclub/evoguess-ai)](https://github.com/aimclub/evoguess-ai/blob/master/LICENSE)
[![Eng](https://img.shields.io/badge/lang-en-yellow.svg)](/README_en.md)
[![Mirror](https://img.shields.io/badge/mirror-github-orange)](https://github.com/aimclub/evoguess-ai)

[//]: # (https://img.shields.io/badge/wiki-documentation-forestgreen)

## Table of contents <a name="tablecontents"></a>
1. [Introduction](intro.md)
2. [Installation](installation.md)
3. [Preliminaries](theory.md)
4. [Input formats](inputs.md)
5. [Basic usage](basic.md)
6. [Advanced usage](advanced.md)
   1. [Mode-independent options](#mio) 
      1. [Input formula](#mio_formula)
      2. [Solver](#mio_solver)
      3. [Limits](#mio_limits)
      4. [Specifying the solving problem (SAT or MaxSAT)](#mio_problem)
      5. [Specifying path to saving logs](#mio_logs)
   2. [ρ-Backdoors mode options](#rho_options)
      1. [MaxSAT problem](#rho_maxsat)
      2. [Arguments of solve function](#rho_solve)
   3. [IBS options](#ibs_options)
   4. [Examples of startup scripts](#examples)
7. [Examples](examples.md)

## Advanced usage

Unlike the [basic usage](basic.md), whose parameters can be controlled 
from the command line, the advanced usage of EvoguessAI assumes that 
the user creates his own startup script following the example described 
below. In this script, the user will have the ability to directly 
influence the way the input formula is processed and additional 
solution parameters that are not available from the command line.

Example of startup script can be found at the end of section.


### Mode-independent options <a name="mio"></a>

Some options are independent of whether ρ-backdoors 
mode or IBS mode is used. The syntax for them is the same in both cases.

#### Input formula <a name="mio_formula"></a>

There are several ways to specify a CNF for solving SAT problems.
The first way: directly specifying the path to the input formula in the CNF format.
```python
from lib_satprob.encoding import CNF

encoding = CNF(from_file='./examples/data/pvs_4_7.cnf')
```
Another way is that WCNF is given as input, but CNF is constructed from it. 
This can be done by using all clauses from WCNF without their weights:
```python
from lib_satprob.encoding import WCNF

encoding = WCNF(from_file='./examples/data/lec_cvk_11.wcnf').unweighted()
```
or by building CNF only from the hard part of WCNF:
```python
from lib_satprob.encoding import WCNF

encoding = WCNF(from_file='./examples/data/lec_cvk_11.wcnf').from_hard()
```

#### Solver <a name="mio_solver"></a>

The creation of the solver instance is done through the `PySatSolver` class:
```python
from lib_satprob.solver import PySatSolver

solver = PySatSolver(sat_name='cad195')
```

#### Limits <a name="mio_limits"></a>

EvoguessAI supports two options for limiting the subsolvers used: 
1. a limit on the solution time:
   ```python
   from function.module.measure import measures
   
   measure = measures.get(f'measure:time')()
   lim = 5
   ```
2. or on the number of conflicts:
      ```python
   from function.module.measure import measures
   
   measure = measures.get(f'measure:conflicts')()
   lim = 20000
   ```

#### Specifying the solving problem <a name="mio_problem"></a>

In both modes EvoguessAI can solve the SAT problem.  
In this case, the `problem` parameter must be set as follows:
```python
from lib_satprob.problem import SatProblem

# An instance of the solver must be created and the encoding must contain CNF.
problem = SatProblem(
            solver, encoding
        )
```

#### Specifying path to saving logs <a name="mio_logs"></a>

User can specify his own directory for saving logs of EvoguessAI functioning. 
A subdirectory named  
`*startdate*-*starttime*_*enddate*-*endtime*` will be created in the specified directory for each individual run.
```python
from utility.work_path import WorkPath

log_path = WorkPath('examples', 'logs')
```

### ρ-Backdoors mode options <a name="rho_options"></a>

In addition to the parameters described above, 
EvoguessAI in ρ-backdoors usage mode depends on a few more.

#### MaxSAT problem <a name="rho_maxsat"></a>

In case the user wants to solve a MaxSAT problem, 
then he needs to create an instance of `WCNF` class as input 
formula and define the `problem` parameter as MaxSAT problem.
```python
from lib_satprob.problem import MaxSatProblem

# An instance of the solver must be created and the encoding must contain WCNF.
problem = MaxSatProblem(
            solver, encoding
        )
```


#### Arguments of solve function <a name="rho_solve"></a>

Start solving SAT or MaxSAT problems using ρ-backdoors by calling `solve()`. 
Its syntax looks as follows:

```python
 report = solve(problem=problem,
                runs=40,
                measure=measure,
                seed_offset=123,
                max_workers=4,
                bd_size=10,
                limit=lim,
                log_path=log_path,
                iter_count=3000)
```
How to set `problem`, `measure`, `limit` and `log_path` parameters is written above.
But also `solve()` depends on several other parameters, which are described below:

+ `runs` Number of runs of the evolutionary algorithm to search for ρ-backdoors. 
Each run performs `iter_count` iterations of the evolutionary algorithm,
ranks all found backdoors by ρ, and returns the backdoor with maximal ρ 
(or several, in case of equal ρ). When EvoguessAI is multithreaded, 
all runs are evenly (as much as possible) distributed among different threads.  
**Default: 40.**


+ `seed_offset` Initial seed for an evolutionary algorithm. 
Obviously, this parameter can influence the search for backdoors, 
but there is little possibility to change it in a meaningful way. 
In any case, in case of unsatisfactory backdoor search results, 
or for research purposes, the user can directly change this parameter 
and evaluate the resulting effect.  
**Default: 123.**


+ `max_workers` The number of available processes for multiprocessing.   
**Default: 4.**


+ `bd_size` The size of the ρ-backdoors being searched for. 
The longer the ρ-backdoors are, the easier are the potential 
subproblems based on them. However, the potential number of hard 
tasks (but not the ρ-value) increases with the ρ-backdoor length. ρ-Backdoors of 
length 10 are used for most problems, but this number can be increased 
if the ρ-backdoors found do not have high ρ-value.  
**Default: 10.**


+ `iter_count` The number of iterations of the 
evolutionary algorithm (by iterations we mean mutations). 
This parameter directly affects the backdoor search process. 
Its increase will lead to slower backdoor search phase, 
but to more successful backdoor search, i.e. to 
finding backdoors with higher ρ-value. 
The default value was chosen empirically.  
**Default: 3000.**

### IBS mode options <a name="ibs_options"></a>

This section needs to be further developed.

### Examples of startup scripts <a name="examples"></a>

Example of solving SAT problem with time limit:
```python
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import SatProblem
from lib_satprob.encoding import CNF


from utility.work_path import WorkPath
from pipeline.rho_solve import solve

from function.module.measure import measures

if __name__ == '__main__':
    encoding = CNF(from_file='./examples/data/pvs_4_7.cnf')
    solver = PySatSolver(sat_name='cad195')
    measure = measures.get(f'measure:time')()
    lim = 5
    log_path = WorkPath('examples', 'logs')
    problem = SatProblem(
                solver, encoding
            )
    report = solve(problem=problem,
                   runs=50,
                   measure=measure,
                   seed_offset=321,
                   max_workers=5,
                   bd_size=12,
                   limit=lim,
                   log_path=log_path,
                   iter_count=4000)
```

Example of solving MaxSAT problem with limit of conflicts:
```python
from lib_satprob.solver import PySatSolver
from lib_satprob.problem import MaxSatProblem
from lib_satprob.encoding import WCNF


from utility.work_path import WorkPath
from pipeline.rho_solve import solve

from function.module.measure import measures

if __name__ == '__main__':
    encoding = WCNF(from_file='./examples/data/pvs_4_7.cnf')
    solver = PySatSolver(sat_name='cad195')
    measure = measures.get(f'measure:conflicts')()
    lim = 20000
    log_path = WorkPath('examples', 'logs')
    problem = MaxSatProblem(
                solver, encoding
            )
    report = solve(problem=problem,
                   runs=40,
                   measure=measure,
                   seed_offset=123,
                   max_workers=4,
                   bd_size=10,
                   limit=lim,
                   log_path=log_path,
                   iter_count=3000)
```


<sup>[&uarr;Table of contents](#tablecontents)</sup>
