Mutation
========

In evolution and genetic algorithms, оператор мутации определяет каким образом будут изменяться исходные особи. Особи определяются массивом бит равной длины. При мутации значения заданных битов инвертируются на противоположные.

Uniform mutation
----------------

При мутации каждый бит с вероятностью равной **flip_scale/array_length** может изменить свое значение на противоположное, где **array_length** is a length of bit array.

.. code-block:: python

   from algorithm.module.mutation import Uniform

    selection = Uniform(
        flip_scale: float = 1.0,
        random_seed: Optional[Int] = None
    )

Doer mutation
-------------

См. статью (добавить ссылку позже).

.. code-block:: python

   from algorithm.module.mutation import Doer

    selection = Doer(
        beta: int = 3,
        random_seed: Optional[Int] = None
    )

Other algorithm modules
-----------------------

* `Crossover <crossover.module.html>`_
* `Selection <selection.module.html>`_
