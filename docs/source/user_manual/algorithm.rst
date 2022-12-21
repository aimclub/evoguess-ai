Algorithm
=========

| This package defines a metaheuristic algorithms for fitness function optimization. All the necessary and optional parameters that determine the behavior of the algorithm are also set here.

Strategy (μ, λ) (Evolution Algorithm)
--------------------------------------

| Реализация эволюционной стратегии **(μ, λ)**.

| Поведения реализуемой стратегии управляется следующими параметрами:

* **mu_size** -- Size of the parent population.
* **lambda_size** -- Size of the offspring population.
* **mutation** -- Instance of `Mutation <algorithm_modules/mutation.module.html>`_ module.
* **selection** -- Instance of `Selection <algorithm_modules/selection.module.html>`_ module.
* **max_queue_size** -- Максимальное число особей, которые могут одновременно находиться в процессе вычисления значение фитнес-функции. По умолчанию значение не задано, то есть одновременно будет вычисления значение фитнес-функции столько особей очередь будет пополняться пока есть свободные вычислительные ресурсы.

.. note::

    **min_update_size** всегда равно **lambda_size**.

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

| Реализация эволюционной стратегии **(μ + λ)**.

| Поведения реализуемой стратегии управляется следующими параметрами:

* **mu_size** -- Size of the parent population.
* **lambda_size** -- Size of the offspring population.
* **mutation** -- Instance of `Mutation <algorithm_modules/mutation.module.html>`_ module.
* **selection** -- Instance of `Selection <algorithm_modules/selection.module.html>`_ module.
* **min_update_size** -- Задает минимальное число новых особей, при котором происходит переход к следующей популяции. Значения от **1** до **lambda_size**. По умолчанию значение равно **1**, то есть переход происходит каждый раз, когда посчитано значение фитнес-функции хотя бы для одной новой особи.
* **max_queue_size** -- Максимальное число особей, которые могут одновременно находиться в процессе вычисления значение фитнес-функции. По умолчанию значение не задано, то есть одновременно будет вычисления значение фитнес-функции столько особей очередь будет пополняться пока есть свободные вычислительные ресурсы.

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

| Реализация генетического алгоритма используя стратегию **Элитизм**. Основная особенность данной стратегии состоит в том, что при переходе от одной популяции к следующей, в следующей популяции обязательно будут сохранено заданное число лучших  особей (элит). Остальные особи постепенно заменяются более свежими.

| Поведения реализуемой стратегии управляется следующими параметрами:

* **population_size** -- Размер популяции без учета элитарных особей.
* **elites_count** - Число элитарных особей, которые всегда переходят в следующую популяцию.
* **mutation** -- Instance of `Mutation <algorithm_modules/mutation.module.html>`_ module.
* **crossover** -- Instance of `Crossover <algorithm_modules/crossover.module.html>`_ module.
* **selection** - Instance of `Selection <algorithm_modules/selection.module.html>`_ module.
* **min_update_size** -- Задает минимальное число новых особей, при котором происходит переход к следующей популяции. Значения от **1** до **population_size**. По умолчанию значение равно **1**, то есть переход происходит каждый раз, когда посчитано значение фитнес-функции хотя бы для одной новой особи.
* **max_queue_size** - Максимальное число особей, которые могут одновременно находиться в процессе вычисления значение фитнес-функции. По умолчанию значение не задано, то есть одновременно будет вычисления значение фитнес-функции столько особей очередь будет пополняться пока есть свободные вычислительные ресурсы.

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