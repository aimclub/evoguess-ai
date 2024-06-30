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
   1. [ρ-Backdoors mode](#rho)
      1. [Usage](#rho_usage)
      2. [Options](#rho_options)
      3. [Description of EvoguessAI workflow in ρ-backdoors mode](#rho_workflow)
   2. [References](#refs)
6. [Advanced usage](advanced.md)
7. [Examples](examples.md)

## Basic usage

There are two variants of EvoguessAI functioning: using ρ-backdoors 
and using Inverse Backdoor Sets.

Basic use suggests running the files `main_rho.py` for rho-backdoors mode 
and `main_ibs.py` for IBS mode, with parameters controlled by command line arguments.

[//]: # (TODO ibs mode)

### ρ-Backdoors mode <a name="rho"></a>

The main mode of EvoguessAI is related to the use of ρ-backdoors 
to solve SAT and MaxSAT problems. 

#### Usage <a name="rho_usage"></a>

In general, the startup looks as follows:
```
main_rho.py [-h] [-s [SOLVERNAME]] [-nr [NOFEARUNS]] [-np [NOFPROCESSES]] [-bds [BACKDOORSIZE]] [-tl [TIMELIMIT]]
                 [-cl [CONFLICTLIMIT]]
                 formula
```

The only mandatory parameter is the input formula. 
For all other parameters, if they are not user-defined, 
the default values are set (the default limit for solving 
hard tasks is set to 20000 conflicts per hard task).


#### Options <a name="rho_options"></a>

+ `-h, --help` Print help message.


+ `formula` Input file with formula in CNF or WCNF format. Note, that parser is checked
format of the file firstly by its extension and secondly by header of the file. 
For example: if file extension is .cnf or .wcnf, Evoguess will start solving SAT 
and MaxSAT problem w.r.t. input formula respectively (without checking header of file). 
Otherwise, Evoguess will open file and check first line (header). If header starts with "p cnf" or
"p wcnf", the solving is started, otherwise the error will be shown.  
**Mandatory positional argument.**


+ `-s, --solvername [NAME]` The name of the solver to be used as the 
SAT oracle to solve the subproblems. This solver will be used 
exactly when solving hard tasks with some constraint, but not 
when searching for the ρ-backdoors themselves. This is because 
only the propagate() function is used to search for ρ-backdoors, 
which is deterministic and independent of the solver used. We chose the
SAT solver Minisat2.2 as the least resource-consuming solver for propagate 
when searching for backdoors. For solving hard tasks, the user can choose 
any of the solvers presented in PySAT. By default, we suggest using Cadical1.9.5 
as the most powerful one.  
**Default: Cadical195.**  
The list of most useful solvers with their acceptable names 
and also links to stand-alone versions
(for more information, see the 
[PySAT solvers documentation](https://pysathq.github.io/docs/html/api/solvers.html)): 
  1. "cd195" &ndash; [CaDiCaL 1.9.5](https://github.com/arminbiere/cadical/releases/tag/rel-1.9.5).
  2. "gc3" &ndash; [Glucose 3](https://github.com/audemard/glucose/releases/tag/3.0).
  3. "gc4" &ndash; [Glucose 4.2.1](https://github.com/audemard/glucose/releases/tag/4.2.1).
  4. "lgl" &ndash; [Lingeling](https://github.com/arminbiere/lingeling/releases/tag/rel-1.0.0).
  5. "mcb" &ndash; [MapleLCMDistChronoBT](https://github.com/krobelus/MapleLCMDistChronoBT).
  6. "m22" &ndash; [MiniSat 2.2](http://minisat.se/downloads/minisat-2.2.0.tar.gz).
  7. "mgh" &ndash; [MiniSat (version from github)](https://github.com/niklasso/minisat).  




+ `-nr, --nofearuns [INT]` Number of runs of the evolutionary algorithm to search for ρ-backdoors. 
Each run performs 3000 iterations of the evolutionary algorithm (1+1 EA [[1]](#1)),
ranks all found backdoors by ρ, and returns the backdoor with maximal ρ 
(or several, in case of equal ρ). When EvoguessAI is multithreaded, 
all runs are evenly (as much as possible) distributed among different threads.  
**Default: 40.**


+ `-np, --nofprocesses [INT]` The number of available processes for multithreading. 
Multithreading is implemented through the ProcessPoolExecutor class of 
the [concurrent.futures module](https://docs.python.org/3/library/concurrent.futures.html).  
**Default: 4.**


+ `-bds, --backdoorsize [INT]` The size of the ρ-backdoors being searched for. 
The longer the ρ-backdoors are, the easier are the potential 
subproblems based on them. However, the potential number of hard 
tasks (but not the ρ-value) increases with the ρ-backdoor length. ρ-Backdoors of 
length 10 are used for most problems, but this number can be increased 
if the ρ-backdoors found do not have high ρ-value.  
**Default: 10.**


+ `-tl, --timelimit [SECONDS]` OR `-cl, --conflictlimit [INT]` 
SAT oracles used in EvoguessAI support two variants of constraints 
when solving hard tasks: by running time or by the number of 
conflicts that occurred during the solution. 
These parameters are mutually exclusive and the maximum 
(in absolute values) of the ones specified by the 
user is selected at startup.  
**If none of the parameters are specified, 
EvoguessAI sets the limit on the number of conflicts to 20000.**


#### Description of EvoguessAI workflow in ρ-backdoors mode <a name="rho_workflow"></a>

EvoguessAI's work in ρ-backdoor's mode 
is divided into 2 phases: ro-backdoor search and problem solving. 

In the first phase, there are [NOFEARUNS] of runs of 
the 1+1 evolutionary algorithm. Each run starts from 
a random point (a random vector of [BACKDOORSIZE] length 
over the variables of the original formula) defined by seed, 
after which, the ρ-value for the given backdoor is computed. 
ρ-Value in short is the ratio of the number of tasks, 
for those propagate gives a conflict to the total number of tasks 
(for detailed information see [Preliminaries](theory.md)).

Then, changes are made in the starting vector according to (1+1)EA 
in order to maximize the ρ-value. After a certain number of iterations 
(3000 by default), the evolutionary algorithm terminates and returns 
the backdoor with the maximum ρ-value among those found 
(or several backdoors, if ρ-value is equal).

If a backdoor with a single hard task is searched, 
unit clauses from it are immediately written to CNF, 
and the corresponding variables are excluded from 
the set of variables used to search for backdoors.

[//]: # (After searching for backdoors, trivial deriving is started,
        which is a process where all backdoors with the same hard task
        are recorded as unit clauses. This fills the set of "covered"
        variables. Next, useless backdoors that do not expand
        the set of variables are weeded out.)

Next, a deriving process is started, which includes 
selection of a backdoor, extraction of easy tasks from it, 
their subsequent writing as a conjunctive normal form (CNF) 
and minimisation using the [Espresso tool](https://github.com/Gigantua/Espresso). 
This process extracts useful information from the backdoors. 
Sorting the backdoors and their subsequent filtering involves 
ordering the remaining backdoors according to the RO value. 
Then a search is made among the sorted backdoors for the one 
that will add the largest number of variables to the set of 
variables across all selected backdoors. This process is repeated 
until no backdoor remains that can add at least one new variable in 
the set of "covered" variables. 

This forms the order of backdoors for further 
Cartesian product during phase 2. 

Example of output for Phase 1:
```shell
00:00:01 ---------------------- Running on 4 threads ----------------------
00:00:01 -------------------------------------------------------------------
00:00:01 ------------------- Phase 1 (Prepare backdoors) -------------------
00:00:01 Searching: 100%|██████████| 40/40 [03:31<00:00,  5.29s/run, 7009 bds]

# In phase 1 7009 backdoors with was found by 40 runs of (1+1)EA. 
# It was backdoors with maximum rho from every run.

00:03:33 Deriving: 100%|██████████| 608/608 [00:52<00:00, 11.65bd/s, 844 clauses]

# During deriving process from all backdoor 844 additional clauses was extract to the original CNF.

00:04:25 ---------------------- Prepared 10 backdoors ----------------------

# All backdoors were filtered from useless ones (not carrying new variables). 
# 10 backdoors left.
```

Phase 2 consists of solving the problem.

During this process, a Cartesian product is built over 
the hard tasks from backdoors, according to the order found 
in phase 1, which increases the length of hard tasks. 
After adding the hard tasks from each new backdoor to the 
Cartesian product, we run the subsolver with a budget 
(limit on the running time or number of conflicts).

All unsolved hard tasks at each stage are sent to the next one, 
where the Cartesian product is again constructed using them 
and hard tasks from the next backdoor in the order and the 
process is repeated.

If the cycle has reached the last backdoor, the budget 
is switched off and all remaining hard tasks are solved to the end.

Example of output for Phase 2:
```shell
00:04:25 -------------------------------------------------------------------
00:04:25 --------------------- Phase 2 (Solve problem) ---------------------
00:04:25 ------------------- Used 2 backdoors (20 vars) -------------------
00:04:25 Sifting: 100%|██████████| 4/4 [00:04<00:00,  1.06s/task, 4 hard]

# Hard tasks from first two backdoor was used to construct Cortesian product. 
# It's lenght is 4 cubes. When solving these 4 cubes with a limit in conflicts, 
# it turned out that all 4 were too difficult. Therefore, we add the next 
# backdoor (builds the Cartesian product of the current set of cubes and 
# the hard tasks from the next backdoor).

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


### References <a name="refs"></a>

<a id="1">[1]</a> 
Droste, Stefan, Thomas Jansen, and Ingo Wegener. 
"On the analysis of the (1+ 1) evolutionary algorithm." 
Theoretical Computer Science 276.1-2 (2002): 51-81.



<sup>[&uarr;Table of contents](#tablecontents)</sup>