Selection
=========

In evolutionary and genetic algorithms, the selection operator is used to select some individuals in the current population to tweak them using `mutation <mutation.module.html>`_ and `crossover <crossover.module.html>`_ operators. Далее измененные особи оцениваются и участвуют при переходе к следующей популяции.

Best-point selection
--------------------

| Выбирает **best_count** лучших особей для tweak operation. Если для выполнения операции tweak выбрано не достаточно особей, то они закольцовываются.
| For example: if **best_count** equals **2**, them selected output is **[s1, s2, s1, s2, s1, s2, ...]**, where **s1** and **s2** are the best points in current population.

.. code-block:: python

   from algorithm.module.selection import BestPoint

    selection = BestPoint(
        best_count: int,
        random_seed: Optional[int] = None
    )

Roulette selection
------------------

Выбирает особи в зависимости от их fitness value. Вероятность того, что особь будет выбрана обратно пропорциональна ее значению фитнеса.

.. code-block:: python

   from algorithm.module.selection import Roulette

    selection = Roulette(
        random_seed: Optional[int] = None
    )

Other algorithm modules
-----------------------

* `Mutation <mutation.module.html>`_
* `Crossover <crossover.module.html>`_
