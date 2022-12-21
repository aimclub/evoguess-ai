Crossover
=========

In genetic algorithms, оператор скрещивания определяет каким образом будут скрещиваться two selected individuals. Особи определяются массивом бит равной длины. При скрещивании заданные биты на одинаковых позициях меняются местами и на выходе получаются две новые особи.

Uniform crossover
-----------------

При скрещивании каждая пара бит может поменяться местами с вероятностью равной **swap_prob**.

.. code-block:: python

   from algorithm.module.crossover import Uniform

    crossover = Uniform(
        swap_prob: float = 0.5,
        random_seed: Optional[int] = None
    )

One-point crossover
-------------------

При скрещивании случайно выбирается индекс **i** внутри массива бит, и каждая пара бит от **0** до **i** меняется местами.

.. code-block:: python

   from algorithm.module.crossover import OnePoint

    crossover = OnePoint(
        random_seed: Optional[int] = None
    )

Two-point crossover
-------------------

При скрещивании случайно выбирается два индекса **i1** и **i2** внутри массива бит, и каждая пара бит от **i1** до **i2** меняется местами.

.. code-block:: python

   from algorithm.module.crossover import TwoPoint

    crossover = TwoPoint(
        random_seed: Optional[int] = None
    )


Other algorithm modules
-----------------------

* `Mutation <mutation.module.html>`_
* `Selection <selection.module.html>`_
