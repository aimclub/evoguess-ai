Algorithm
=========

| This package defines a metaheuristic algorithms for fitness `Function <function.html>`_ optimization. All the necessary and optional parameters that determine the behavior of the algorithm are also set here.

Strategy (μ, λ) (Evolution Algorithm)
--------------------------------------

| Implementation of evolutionary strategy **(μ, λ)**. The behavior of this implementation is controlled by the following parameters:

* **mutation** -- An instance of the `Mutation <algorithm_modules/mutation.module.html>`_ module.
* **selection** -- An instance of the `Selection <algorithm_modules/selection.module.html>`_ module.
* **mu_size** -- The size of the parent population.
* **lambda_size** -- The size of the offspring population.
* **max_queue_size** -- The maximum number of processed individuals at the same time, for which the fitness function values is calculated. By default, the value is not set, that is, the number of  processed individuals at the same time will depend on the amount of allocated computing resources through the `Executor <executor.html>`_ instance.

.. note::

    **min_update_size** is always equal to **lambda_size**.

.. code-block:: python

   from algorithm.impl import MuPlusLambda

    algorithm = MuPlusLambda(
        mu_size: int,
        lambda_size: int,
        mutation: Mutation,
        selection: Selection,
        max_queue_size: Optional[int]
    )


Strategy (μ + λ) (Evolution Algorithm)
--------------------------------------

| Implementation of evolutionary strategy **(μ + λ)**. The behavior of this implementation is controlled by the following parameters:

* **mutation** -- An instance of the `Mutation <algorithm_modules/mutation.module.html>`_ module.
* **selection** -- An instance of the `Selection <algorithm_modules/selection.module.html>`_ module.
* **mu_size** -- The size of the parent population.
* **lambda_size** -- The size of the offspring population.
* **min_update_size** -- The minimum number of new individuals at which a transition to the next population occurs. Values from **1** to **population_size**. By default, the value is **1**, i.e. the transition occurs every time the fitness function value is calculated for at least one new individual.
* **max_queue_size** -- The maximum number of processed individuals at the same time, for which the fitness function values is calculated. By default, the value is not set, that is, the number of  processed individuals at the same time will depend on the amount of allocated computing resources through the `Executor <executor.html>`_ instance.

.. code-block:: python

   from algorithm.impl import MuPlusLambda

    algorithm = MuPlusLambda(
        mu_size: int,
        lambda_size: int,
        mutation: Mutation,
        selection: Selection,
        min_update_size: int = 1,
        max_queue_size: Optional[int] = None
    )


Elitism (Genetic Algorithm)
---------------------------

| Implementation of a genetic algorithm using the **Elitism** strategy. The main feature of this strategy is that the transition to the next population occurs while maintaining a given number of the best individuals (elites). The remaining individuals are gradually replaced by more recent ones.
| The behavior of this implementation is controlled by the following parameters:

* **mutation** -- An instance of the `Mutation <algorithm_modules/mutation.module.html>`_ module.
* **crossover** -- An instance of the`Crossover <algorithm_modules/crossover.module.html>`_ module.
* **selection** - An instance of the `Selection <algorithm_modules/selection.module.html>`_ module.
* **population_size** -- The size of population excluding elite's individuals.
* **elites_count** - The number of elite's individuals that always move to the next population.
* **min_update_size** -- The minimum number of new individuals at which a transition to the next population occurs. Values from **1** to **population_size**. By default, the value is **1**, i.e. the transition occurs every time the fitness function value is calculated for at least one new individual.
* **max_queue_size** - The maximum number of processed individuals at the same time, for which the fitness function values is calculated. By default, the value is not set, that is, the number of  processed individuals at the same time will depend on the amount of allocated computing resources through the `Executor <executor.html>`_ instance.

.. code-block:: python

   from algorithm.impl import Elitism

    algorithm = Elitism(
        population_size: int,
        elites_count: int,
        mutation: Mutation,
        crossover: Crossover,
        selection: Selection,
        min_update_size: int = 1,
        max_queue_size: Optional[int] = None
    )

Algorithm modules
-----------------

.. toctree::
    :maxdepth: 1

    algorithm_modules/mutation.module
    algorithm_modules/crossover.module
    algorithm_modules/selection.module