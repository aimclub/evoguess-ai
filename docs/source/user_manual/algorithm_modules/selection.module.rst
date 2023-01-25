Selection
=========

| In evolutionary and genetic algorithms, the selection operator is used to select some individuals in the current population to tweak them using `mutation <mutation.module.html>`_ and `crossover <crossover.module.html>`_ operators. The population is type of `Vector <../core_models/point.model.html#vector>`_, which is an alias for a list of `Point <../core_models/point.model.html>`_.

.. code-block:: python

    class Selection:
        def select(population: Vector, size: int) -> Vector:

| The **select** method returns a new list of individuals of length **size**, which are selected from the passed **population**.

Best-point selection
--------------------

Selects the **best_count** of the best individuals from the **population**. If the number of requested individuals **size** is greater than **best_count**, then individuals from **best_count** are reselected. The selected individuals are shuffled randomly using the passed **random seed**.

.. note::
    If, for example, **best_count** is equal to **2**, then selected output is **[p1, p2, p1, p2, p1, p2, ...]**, where **p1** and **p2** are the best points in current population.

.. code-block:: python

   from algorithm.module.selection import BestPoint

    selection = BestPoint(
        best_count: int,
        random_seed: Optional[int] = None
    )

Roulette selection
------------------

Selects **size** individuals from the **population** based on their fitness value. The probability that an individual will be selected is inversely proportional of its fitness value. The selected individuals are shuffled randomly using the passed **random seed**.

.. code-block:: python

   from algorithm.module.selection import Roulette

    selection = Roulette(
        random_seed: Optional[int] = None
    )

Other algorithm modules
-----------------------

* `Mutation <mutation.module.html>`_
* `Crossover <crossover.module.html>`_
