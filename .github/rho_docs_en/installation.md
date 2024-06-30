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
   1. [Used packages](#packages)
      1. [Requirement packages](#packages_req)
      2. [Optional packages](#packages_optional)
3. [Preliminaries](theory.md)
4. [Input formats](inputs.md)
5. [Basic usage](basic.md)
6. [Advanced usage](advanced.md)
7. [Examples](examples.md)

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

### Used packages <a name="packages"></a>

Although all required packages can be installed using the requirements.txt 
and requirements-mpi.txt files, we will provide here a brief description 
of them and how to install them separately.

#### Requirement packages <a name="packages_req"></a>
1. [numpy](https://numpy.org/) (>=1.21.6) – a Python library used for working with arrays. 
It also has functions for working in domain of linear algebra, 
fourier transform, and matrices. NumPy is used in almost every field of 
science and engineering, so EvoguessAI also uses it for the most 
convenient representation of such objects as binary vectors, 
backdoors, sets of variables, etc.
   > pip install numpy

2. [python-sat](https://pysathq.github.io/) (>=1.8.dev4) – PySAT is a toolkit 
that provides extremely convenient functionality for using SAT oracles. 
It allows to use both polynomial subsolvers for SAT 
solving (e.g. Unit Propagation) and state-of-the-art 
SAT solvers, such as Glucose, Cadical, MapleChrono 
and many others (see list of 
[PySAT supported solvers](https://pysathq.github.io/docs/html/api/solvers.html#list-of-classes)).
In EvoguessAI PySAT is used to represent 
input formulas (CNF and WCNF), as a polynomial algorithm 
when searching for ρ-backdoors and as a SAT oracle when 
solving subproblems from decompositions.
   > pip install python-sat


#### Optional packages <a name="packages_optional"></a>

1. [tqdm](https://tqdm.github.io/) – package, that provide tools to show 
smart progress meter of work process.
   > pip install tqdm

2. [mpi4py](https://mpi4py.readthedocs.io/en/stable/) – MPI for Python 
provides Python bindings for the Message Passing Interface (MPI) 
standard, allowing Python applications to exploit multiple 
processors on workstations, clusters and supercomputers.
   > pip install mpi4py

<sup>[&uarr;Table of contents](#tablecontents)</sup>