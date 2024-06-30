# EvoGuessAI
[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)

[![license](https://img.shields.io/github/license/aimclub/evoguess-ai)](https://github.com/aimclub/evoguess-ai/blob/master/LICENSE)
[![Eng](https://img.shields.io/badge/lang-en-yellow.svg)](/README_en.md)
[![Mirror](https://img.shields.io/badge/mirror-github-orange)](https://github.com/aimclub/evoguess-ai)

[//]: # ( TODO
2. бэдж "документации": https://img.shields.io/badge/wiki-documentation-forestgreen
)

## Table of contents <a name="tablecontents"></a>
1. [Introduction](intro.md)
2. [Installation](installation.md)
3. [Preliminaries](theory.md)
4. [Input formats](inputs.md)
   1. [CNF in DIMACS format](#cnf)
   2. [WCNF in DIMACS format](#wcnf)
5. [Basic usage](basic.md)
6. [Advanced usage](advanced.md)
7. [Examples](examples.md)

## Input formats

EvoguessAI can accept CNF and WCNF in DIMACS format 
as input formula. The following sections describe what this is.

#### CNF in DIMACS format <a name="cnf"></a>

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
CNF in example contains `2` clauses over the set of `3` variables.

#### WCNF in DIMACS format  <a name="wcnf"></a>

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

[WCNF in DIMACS](http://www.maxhs.org/docs/wdimacs.html) format has a little changes compare to CNF: 
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
10 -1 2 3 0
10 -1 -2 -3 -4 0
```
WCNF in example contains `5` clauses over the set of `4` variables. 
Weight for hard clauses is `10`.
First 3 clauses are soft ones, with different weights for each (`1`, `3` and `4`).
Last 2 clauses are hard ones.


<sup>[&uarr;Table of contents](#tablecontents)</sup>
