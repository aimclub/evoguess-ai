# EvoGuessAI
[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)

[![license](https://img.shields.io/github/license/aimclub/evoguess-ai)](https://github.com/aimclub/evoguess-ai/blob/master/LICENSE)
[![Eng](https://img.shields.io/badge/lang-ru-yellow.svg)](/README.md)
[![Mirror](https://img.shields.io/badge/mirror-GitLab-orange)](https://gitlab.actcognitive.org/itmo-sai-code/evoguess-ai)

## Table of contents  <a name="tablecontents"></a>
1. [Introduction](intro.md)
2. [Installation](installation.md)
3. [Preliminaries](theory.md)
4. [Basic usage](basic.md)
5. [Advanced usage](advanced.md)
6. [Examples](examples.md)

## Basic usage

There are two main modes of EvoguessAI functioning: using ρ-backdoors 
and using Inverse Backdoor Sets.

In the following we will describe the command line parameters that control 
each mode of operation, as well as the default startup options.

### ρ-Backdoors mode

The main mode of EvoguessAI is related to the use of ρ-backdoors 
to solve SAT and MaxSAT problems. 

There are several command line parameters that affect this mode.

#### Options

+ `-h, --help` Print help message.


+ `-f, --formula [FILE]` Input file with formula in CNF or WCNF format. Note, that parser is checked
format of the file firstly by its extension and secondly by header of the file. 
For example: if file extension is .cnf or .wcnf, Evoguess will start solving SAT 
and MaxSAT problem w.r.t. input formula respectively (without checking header of file). 
Otherwise, Evoguess will open file and check first line (header). If header starts with "p cnf" or
"p wcnf", the solving is started, otherwise the error will be shown.  
**Mandatory option.**


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

#### Usage

All basic startup parameters are controlled by command line arguments.
In general, the startup looks as follows:
```
main_p.py [-h] -f FORMULA [-s [SOLVERNAME]] [-nr [NOFEARUNS]] [-seed [SEEDINITEA]] [-np [NOFPROCESSES]]
                 [-bds [BACKDOORSIZE]] [-tl [TIMELIMIT]] [-cl [CONFLICTLIMIT]]
```

The only mandatory parameter is the input formula. 
For all other parameters, if they are not user-defined, 
the default values are set (the default limit for solving 
hard tasks is set to 20000 conflicts per hard task).

EvoguessAI's work in ρ-backdoor's mode 
is divided into 2 phases: ro-backdoor search and problem solving. 

In the first phase, there are [NOFEARUNS] of runs of 
the 1+1 evolutionary algorithm. Each run starts from 
a random point (a random vector of [BACKDOORSIZE] length 
over the variables of the original formula) defined by seed, 
after which, the ρ-value for the given backdoor is computed. 
ρ-Value in short is the ratio of the number of tasks solved 
for a given constraint to the total number of tasks 
(for detailed information see [Preliminaries](theory.md)).

Then, changes are made in the starting vector according to (1+1)EA 
in order to maximize the ρ-value. After a certain number of iterations 
(3000 by default), the evolutionary algorithm terminates and returns 
the backdoor with the maximum ρ-value among those found 
(or several backdoors, if ρ-value is equal).



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



### References

<a id="1">[1]</a> 
Droste, Stefan, Thomas Jansen, and Ingo Wegener. 
"On the analysis of the (1+ 1) evolutionary algorithm." 
Theoretical Computer Science 276.1-2 (2002): 51-81.



<sup>[&uarr;Table of contents](#tablecontents)</sup>