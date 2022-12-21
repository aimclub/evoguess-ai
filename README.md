# EvoGuessAI

Component for finding decomposition sets and estimating hardness of SAT instances. The search for decomposition sets is realized via the optimization of the special pseudo-Boolean black-box functions that estimate the hardness of the decomposition corresponding to the employed decomposition method and the considered set. To optimize the value of such functions the framework uses metaheuristic algorithms, in particular, the evolutionary ones.

## Installation

At the moment, only manual installation is available.

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

## Documentation

Documentation is available [here](https://evoguess-ai.readthedocs.io/) and includes installation instructions and base usage manual.