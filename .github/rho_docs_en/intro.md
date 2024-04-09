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

## Introduction

EvoGuessAI is a library designed for solving combinatorial problems with Boolean constraints, 
whose main algorithms use so-called probabilistic backdoors. 
The methodology of EvoGuessAI is to find probabilistic backdoors (ρ-backdoors) and then 
use them to solve hard variants of Boolean Satisfiability Problem (SAT), 
Maximum Satisfiability Problem (MaxSAT) and 0-1 Integer Linear 
Programming Problem (0-1-ILP). Let us briefly describe the basic concept 
of applying probabilistic backdoors to solve problems of the described classes.

Strong Backdoor Set (SBS) for a particular combinatorial 
Constraint Satisfaction Problem (SCP) is a set of variables in 
the constraint system under consideration, the knowledge of which 
provides some additional information, often allowing either to 
solve the CSP under consideration significantly faster than by 
brute force, or to construct a non-trivial certificate of 
inconsistency of the given system. 
The exact definition of SBS was given in [[1]](#1). 
Unfortunately, SBS of small size in combinatorial 
problems of the above classes are very rare. 
Moreover, the search for the minimal SBS is an extremely hard problem, 
the upper estimate of the complexity of which is worse than the 
upper estimate of the solution of the considered CSP by the brute 
force method. The so-called probabilistic backdoors or ρ-backdoors, first described 
in [[2]](#2), proved to be more practically suitable. Unlike SBS, a ρ-backdoor 
is not obliged to give a solution to the CSP under consideration, 
but gives only a partial certificate of its inconsistency 
(unsatisfiability in the case of Boolean formulas). However, small-size 
ρ-backdoors exist in many practical examples of CSPs. In addition, 
metaheuristic optimization algorithms can be used to find ρ-backdoors, 
which turn out to be very effective in practice. By knowing some 
set of ρ-backdoors, it is often possible to transform the original 
hard problem into a variant that is not extremely hard for 
the basic combinatorial algorithms being used (SAT, MaxSAT, MIP solvers).
Currently, backdoor-based algorithms and techniques 
have been successfully applied to problems in the following 
areas: Logical Equivalence Checking (LEC), Location Problems, 
Job-Shop Scheduling problems, and cryptographic function 
robustness analysis. 

For more detailed description of the theoretical 
background behind EvoGuessAI, see [Preliminaries](theory.md).


### References

<a id="1">[1]</a> 
Williams R., Gomes C., Selman B. 
Backdoors to typical case complexity. 
IJCAI 2003.

<a id="2">[2]</a>
Semenov A., Pavlenko A., Chivilikhin D., Kochemazov S. 
On probabilistic generalization of backdoors in Boolean satisfiability. 
AAAI 2022.

<sup>[&uarr;Table of contents](#tablecontents)</sup>
