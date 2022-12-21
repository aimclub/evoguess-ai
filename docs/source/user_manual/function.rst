Function
========

This package is used to evaluate fitness values for decomposition sets.

Guess-and-determine
-------------------

| Реализация оценочной функции из статьи (...) для поиска ослабляющих backdoor sets.
| Оценка производится на случайной выборке задач, генерация которой управляется в `Sampling <function_modules/solver.module.html>`_ module. Для каждой задачи выбираются случайные значения для переменных входящих в оцениваемый backdoor. Так же генерируются дополнительные правильные значения переменных, если это необходимо (например при работе с криптографическими функциями).

| Поведение реализуемой функции управляется следующими параметрами:

* **solver** -- Instance of `Solver <function_modules/solver.module.html>`_ module.
* **measure** -- Instance of `Measure <function_modules/measure.module.html>`_ module.

.. code-block:: python

    from function.impl import GuessAndDetermine

    function = GuessAndDetermine(
        solver: Solver
        measure: Measure
    )

Inverse Backdoor Sets
---------------------

| Реализация оценочной функции из статьи (...) предназначенная для поиска inverse backdoor sets в криптографических функциях.
| Оценка производится на случайной выборке задач, генерация которой управляется в `Sampling <function_modules/solver.module.html>`_ module. Для каждой задачи выбирается случайное соответствие (секретный ключ, ключевой поток), и выполняется подстановка правильных значений в исходную формулу с учетом оцениваемого backdoor.

| Поведение реализуемой функции управляется следующими параметрами:

* **solver** -- Instance of `Solver <function_modules/solver.module.html>`_ module.
* **measure** -- Instance of `Measure <function_modules/measure.module.html>`_ module.

.. note::
    Для корректного работы данной оценочного функции необходимо указать  значение параметра **budget** для модуля `Measure <function_modules/measure.module.html>`_.

.. code-block:: python

    from function.impl import InverseBackdoorSets

    function = InverseBackdoorSets(
        solver: Solver
        measure: Measure
    )

Rho Function
------------

| Реализация оценочной функции из статьи (...). Алгоритм работы схож с реализацией Guess-and-Determine, однако solver используется только в режиме Unit Propagation.

| Поведение реализуемой функции управляется следующими параметрами:

* **solver** -- Instance of `Solver <function_modules/solver.module.html>`_ module.
* **measure** -- Instance of `Measure <function_modules/measure.module.html>`_ module.

.. code-block:: python

    from function.impl import RhoFunction

    function = RhoFunction(
        solver: Solver
        measure: Measure
    )

Function modules
----------------

.. toctree::
    :maxdepth: 1

    function_modules/solver.module
    function_modules/measure.module
