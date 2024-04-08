# EvoGuessAI

## Table of contents 
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

+ `-f, --formula [FILE]` Input file with formula in CNF or WCNF format. Note, that parser is checked
format of the file firstly by its extension and secondly by header of the file. 
For example: if file extension is .cnf or .wcnf, Evoguess will start solving SAT 
and MaxSAT problem w.r.t. input formula respectively (without checking header of file). 
Otherwise, Evoguess will open file and check first line (header). If header starts with "p cnf" or
"p wcnf", the solving is started, otherwise the error will be shown.


+ `-s, --solvername [NAME]` The name of the solver to be used as the 
SAT oracle to solve the subproblems. This solver will be used 
exactly when solving hard tasks with some constraint, but not 
when searching for the rho-backdoors themselves. This is because 
only the propagate() function is used to search for rho-backdoors, 
which is deterministic and independent of the solver used. We chose the
SAT solver Minisat2.2 as the least resource-consuming solver for propagate 
when searching for backdoors. For solving hard tasks, the user can choose 
any of the solvers presented in PySAT. By default, we suggest using Cadical1.9.5 
as the most powerful one. The list of most useful solvers with their acceptable names 
and also link to stand-alone versions
(for more information, see the 
[PySAT documentation](https://pysathq.github.io/docs/html/api/solvers.html)): 
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


+ `-np, --nofprocesses [INT]` The number of available processes for multithreading. 
Multithreading is implemented through the ProcessPoolExecutor class of 
the [concurrent.futures module](https://docs.python.org/3/library/concurrent.futures.html).  


+ `-bds, --backdoorsize [INT]` The size of the ρ-backdoors being searched for. 
The longer the ρ-backdoors are, the easier are the potential 
subproblems based on them. However, the potential number of hard 
tasks (but not the ρ-value) increases with the ρ-backdoor length. ρ-Backdoors of 
length 10 are used for most problems, but this number can be increased 
if the ρ-backdoors found do not have high ρ-value.


+ `-tl, --timelimit [SECONDS]` OR `-cl, --conflictlimit [INT]` 
SAT oracles used in EvoguessAI support two variants of constraints 
when solving hard tasks: by running time or by the number of 
conflicts that occurred during the solution. 
These parameters are mutually exclusive and the maximum 
(in absolute values) of the ones specified by the 
user is selected at startup. Accordingly, at least one of the 
parameters must be specified explicitly.


### References

<a id="1">[1]</a> 
Droste, Stefan, Thomas Jansen, and Ingo Wegener. 
"On the analysis of the (1+ 1) evolutionary algorithm." 
Theoretical Computer Science 276.1-2 (2002): 51-81.