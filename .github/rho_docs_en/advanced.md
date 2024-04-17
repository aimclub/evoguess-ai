# EvoGuessAI
[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)

[![license](https://img.shields.io/github/license/aimclub/evoguess-ai)](https://github.com/aimclub/evoguess-ai/blob/master/LICENSE)
[![Eng](https://img.shields.io/badge/lang-ru-yellow.svg)](/README.md)
[![Mirror](https://img.shields.io/badge/mirror-GitLab-orange)](https://gitlab.actcognitive.org/itmo-sai-code/evoguess-ai)

## Table of contents <a name="tablecontents"></a>
1. [Introduction](intro.md)
2. [Installation](installation.md)
3. [Preliminaries](theory.md)
4. [Basic usage](basic.md)
5. [Advanced usage](advanced.md)
6. [Examples](examples.md)

## Advanced usage

### Advanced parameters

EvoguessAI is affected by several parameters controlled from 
the startup script rather than from the command line.

Launching the solution in this script looks as follows:
```python
    report = solve(problem=problem,
                   runs=nof_ea_runs,
                   measure=measure,
                   seed_offset=123,
                   max_workers=workers,
                   bd_size=bds,
                   limit=lim,
                   log_path=None,
                   iter_count=3000)
```
Such parameters as `problem`, `runs`, `max_workers`, `bd_size` and 
`limit` in this fragment of the startup script are command-line 
controlled and described in [Basic usage](basic.md).

Advanced parameters are set empirically by default, 
but the user can control them directly by editing the script if needed.

List of advanced parameters:

+ `seed_offset` Initial seed for an evolutionary algorithm. 
Obviously, this parameter can influence the search for backdoors, 
but there is little possibility to change it in a meaningful way. 
In any case, in case of unsatisfactory backdoor search results, 
or for research purposes, the user can directly change this parameter 
and evaluate the resulting effect.  
**Default: 123.**


+ `log_path` Path to save the logs of EvoguessAI work. 
If the parameter is not specified explicitly, the directory 
**"./examples/logs/rho_solve/*date_time_start_date_time_finish*"**
is created for each EvoguessAI start (for example: 
**"./examples/logs/rho_solve/2024.04.10-11&#xb7;25&#xb7;
40_2024.04.10-11&#xb7;26&#xb7;22/"**). 
Information about EvoguessAI operation during a particular 
run is contained in a file named **meta.json** inside 
the created directory.  
**Default value: None.**

[//]: # (Бтв в логах инфа только про найденные бэкдоры, 
и ничего про дерайвинг и дальнейшее решение. 
Это надо доработать.)

+ `iter_count` The number of iterations of the 
evolutionary algorithm (by iterations we mean mutations). 
This parameter directly affects the backdoor search process. 
Its increase will lead to slower backdoor search phase, 
but to more successful backdoor search, i.e. to 
finding backdoors with higher ρ-value. 
The default value was chosen empirically.  
**Default: 3000.**

[//]: # (Тут нужно добавить, что при нахождении бэкдора с одной 
хардтаской и выделения из неё юнитов, происходит перезапуск 
эволюционки \(в рамках того же "запуска"\), но число итераций 
сохраняется на все такие перезапуски.)

### Input formulas

EvoguessAI can accept CNF and WCNF in DIMACS format 
as input formula. The following sections describe what this is.

#### CNF in DIMACS format

[Conjunctive Normal Form (CNF)](https://en.wikipedia.org/wiki/Conjunctive_normal_form)
is a way of representing logical expressions in Boolean algebra 
that uses conjunction (logical `AND`) and disjunction 
(logical `OR`) of variables and their negations. A CNF is the 
conjunction of several disjunctions, each containing one 
or more variables or their negations. In order to express a logical 
expression into a CNF, the following steps must be performed:
+ **Convert to a DNF (disjunctive normal form).**
This is done by applying de Morgan's laws and other conversion rules.
+ **Simplification of the expression.** 
Absorption laws and other simplification rules are used.
+ **Conversion to a CNF.** The final step is to 
convert each disjunction in parentheses into a 
conjunction using the law of distributivity.

[**DIMACS**](https://jix.github.io/varisat/manual/0.2.0/formats/dimacs.html) 
is a textual format for representing formulas 
in conjunctive normal form, used for Boolean 
satisfiability problems (SAT). In this format, each 
line of a file corresponds to one of the following 
elements:
+ **Comments**: begin with the character `c` and can be anywhere in the file.
+ **Header**: is a string of the form  
`p cnf <number of variables> <number of disjuncts>`.
+ **Disjuncts (or clauses)**: a sequence of numbers separated by spaces, 
which are represent a set of literals connected by a logical `OR`. 
Each literal is represented by a positive integer that corresponds 
to a variable, or a negative integer that corresponds to the negation 
of a variable. Each clause is terminated with zero.

Example of CNF in DIMACS format:
```
p cnf 3 2
1 2 -3 0
-2 3 0
```
CNF in example contains 2 clauses over the set of 3 variables.

#### WCNF in DIMACS format

WCNF (Weighted Conjunctive Normal Form) is an extension of CNF 
that adds weights to individual clauses. The weights are used 
to indicate the importance of each clause in the formula. 
WCNF is used in optimisation problems where the goal is to 
find a solution that maximises or minimises the total cost 
represented by the weights of the clauses.

In practice, when solving a MaxSAT problem, all clauses in the 
WCNF are divided into two parts: hard clauses, which must be 
satisfied in any case, and soft clauses, which can be given a weight, 
and the number (or total weight) of satisfied soft clauses 
must be maximised when solving the MaxSAT problem.

WCNF in DIMACS format has a little changes compare to CNF: 
each clause is preceded by its weight, with the particular 
weight value specified in the header indicating that the 
clause belongs to the hard part. Sctructure of WCNF file:  
+ **Comments**: begin with the character `c` and can be anywhere in the file.
+ **Header**: is a string of the form  
`p wcnf <number of variables> <number of disjuncts> <hard clauses weight>`.
+ **Disjuncts (or clauses)**: a sequence of numbers separated by spaces, 
first of which corresponds to weight of that particular clause, and other are
represent a set of literals connected by a logical `OR`. 
Each literal is represented by a positive integer that corresponds 
to a variable, or a negative integer that corresponds to the negation 
of a variable. Each clause is terminated with zero.

Example of WCNF in DIMACS format:
```
p wcnf 5 4 10
1 1 2 0
3 -2 3 -4 0
4 4 0
10 -1 0
10 -1 -2 -3 -4 -5 0
```
WCNF in example contains 5 clauses over the set of 4 variables. 
First 3 clauses is soft ones, with different weights for each.
Last 2 clauses is hard ones.



<sup>[&uarr;Table of contents](#tablecontents)</sup>
