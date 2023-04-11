Function
========

This package is used to evaluate fitness values for `backdoors <instance_modules/variables.module.html#backdoor>`_.

Guess-and-determine
-------------------

| Implementation of the fitness function from (...) to find weakening sets of variables (aka backdoors). The fitness value is calculated on a random sample of tasks that is generated in `Sampling <core_modules/sampling.module.html>`_ module. For each task, random substitutions are selected for variables from the evaluated backdoor. If necessary, additional correct values of variables are also generated (for example, when processing cryptographic functions).
| The behavior of this implementation is controlled by the following parameters:

* **solver** -- An instance of the `Solver <function_modules/solver.module.html>`_ module.
* **measure** -- An instance of the `Measure <function_modules/measure.module.html>`_ module.

.. code-block:: python

    from function.impl import GuessAndDetermine

    function = GuessAndDetermine(
        solver: Solver
        measure: Measure
    )

Inverse Backdoor Sets
---------------------

| Implementation of the fitness function from [AAAI2018]_ designed to search inverse backdoor sets in cryptographic functions. The fitness value is calculated on a random sample of tasks that is generated in `Sampling <core_modules/sampling.module.html>`_ module. For each task, a random correct substitution for the pair (input set, output set) is selected, and the generated values for the estimated backdoor and output set variables are substituted into the original formula.
| The behavior of this implementation is controlled by the following parameters:

* **solver** -- An instance of the `Solver <function_modules/solver.module.html>`_ module.
* **measure** -- An instance of the `Measure <function_modules/measure.module.html>`_ module.

.. note::
    For this evaluation function to work correctly, you must specify the value of the **budget** parameter for the `Measure <function_modules/measure.module.html>`_ module.

.. code-block:: python

    from function.impl import InverseBackdoorSets

    function = InverseBackdoorSets(
        solver: Solver
        measure: Measure
    )

Rho Function
------------

| Implementation of the fitness function from [AAAI2022]_. This implementation is based on **Guess-and-Determine** function, however, the solver is used only in Unit Propagation mode.
| The behavior of this implementation is controlled by the following parameters:

* **solver** -- An instance of the `Solver <function_modules/solver.module.html>`_ module.
* **measure** -- An instance of the `Measure <function_modules/measure.module.html>`_ module.
* **penalty_power** -- The multiplier for the penalty component in fitness value.

.. code-block:: python

    from function.impl import RhoFunction

    function = RhoFunction(
        solver: Solver
        measure: Measure,
        penalty_power: float
    )

Inverse Polynomial Sets
-----------------------
This implementation is based on **Inverse Backdoor Sets** function, .... The behavior of this implementation is controlled by the following parameters:

* **solver** -- An instance of the `Solver <function_modules/solver.module.html>`_ module.
* **measure** -- An instance of the `Measure <function_modules/measure.module.html>`_ module.
* **min_solved** -- The proportion of tasks in from the random sample for which a resolving substitution of values must be found. Default: 0.

.. code-block:: python

    from function.impl import InversePolynomialSets

    function = InversePolynomialSets(
        solver: Solver
        measure: Measure,
        min_solved: float
    )

Function modules
----------------

.. toctree::
    :maxdepth: 1

    function_modules/solver.module
    function_modules/measure.module
