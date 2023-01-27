# EvoGuessAI

Component for finding decomposition sets and estimating hardness of SAT instances. The search for decomposition sets is realized via the optimization of the special pseudo-Boolean black-box functions that estimate the hardness of the decomposition corresponding to the employed decomposition method and the considered set. To optimize the value of such functions the component uses metaheuristic algorithms, in particular, the evolutionary ones.

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

### How to MPI use

The EvoGuessAI can be run in MPI mode as follows:

```shell script
mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main.py
```

where **perhost** is MPI workers processes on one node, and **workers** is a total MPI workers processes on all dedicated nodes.

## Usage examples

An example of [probabilistic backdoors searching](https://github.com/aimclub/evoguess-ai/blob/master/examples/pvs_search_example.py) to solve the equivalence checking problem of two Boolean schemes that implement different algorithms, using the example of PvS 7x4 encoding (Pancake vs Selection sort).

```python
root_path = WorkPath('examples')
data_path = root_path.to_path('data')
cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
logs_path = root_path.to_path('logs', 'pvs_4_7')
solution = Optimize(
    space=RhoSubset(
        by_mask=[],
        of_size=200,
        variables=Interval(start=1, length=1213)
    ),
    instance=Instance(
        encoding=CNF(from_file=cnf_file)
    ),
    executor=ProcessExecutor(max_workers=16),
    sampling=Const(size=8192, split_into=2048),
    function=RhoFunction(
        penalty_power=2 ** 20,
        measure=Propagations(),
        solver=pysat.Glucose3()
    ),
    algorithm=Elitism(
        elites_count=2,
        population_size=6,
        mutation=Doer(),
        crossover=TwoPoint(),
        selection=Roulette(),
        min_update_size=6
    ),
    limitation=WallTime(from_string='02:00:00'),
    comparator=MinValueMaxSize(),
    logger=OptimizeLogger(logs_path),
).launch()
```

Further, the corresponding problem of checking the equivalence of two Boolean schemes using the example of PvS 7x4 encoding can be [solved using the found backdoors](https://github.com/aimclub/evoguess-ai/blob/master/examples/pvs_solve_example.py) as follows:

```python
root_path = WorkPath('examples')
data_path = root_path.to_path('data')
cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
logs_path = root_path.to_path('logs', 'pvs_4_7_comb')
estimation = Combine(
    instance=Instance(
        encoding=CNF(from_file=cnf_file)
    ),
    measure=SolvingTime(),
    solver=pysat.Glucose3(),
    logger=OptimizeLogger(logs_path),
    executor=ProcessExecutor(max_workers=16)
).launch(*backdoors)
```

Other [examples](https://github.com/aimclub/evoguess-ai/tree/master/examples) can be found in the corresponding project directory.

## Supported by

The study is supported by the Research Center Strong Artificial Intelligence in Industry of ITMO University.

<img src='https://gitlab.actcognitive.org/itmo-sai-code/organ/-/raw/main/docs/AIM-Strong_Sign_Norm-01_Colors.svg' width='200'>

## Documentation

Documentation is available [here](https://evoguess-ai.readthedocs.io/) and includes installation instructions and base usage manual.
