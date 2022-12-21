Core
====

Главный пакет библиотеки EvoGuess. В ядре описывается логика взаимодействия всех зависимых модулей для выполнения требуемой задачи. Основная задача, которую позволяет решить библиотека EvoGuess, является задача метаэвристической оптимизации целевой black-box function.

Optimize
--------

| Данная реализация выполняет оптимизацию целевой **function** с помощью метаэвристического **algorithm** над множеством переменных, которые определяются in search **space**. Значения фитнеса для потенциальных решений вычисляются над выборкой задающейся модулем **sampling** и сравниваются по правилам описанным в модуле **comparator**. Оптимизация осуществляется с использованием вычислительных мощностей заданных in **executor** и ограниченных с помощью модуля **limitation**. Задачей оптимизации выступает **instance**. Процесс оптимизации записывается **logger** в файл в указанном формате.
| Процесс оптимизации зависит от следующих параметров:

* **space** -- Instance of `Space <core_modules/space.module.html>`_ module.
* **logger** -- Instance of Logger in `Output <output.html>`_ package.
* **executor** -- Instance of Executor in `Executor <executor.html>`_ package.
* **instance** -- Instance of Instance in `Instance <instance.html>`_ package. :)
* **sampling** -- Instance of `Sampling <core_modules/sampling.module.html>`_ module.
* **function** -- Instance of Function in `Function <function.html>`_ package.
* **algorithm** -- Instance of Algorithm in `Algorithm <algorithm.html>`_ package.
* **comparator** -- Instance of `Comparator <core_modules/comparator.module.html>`_ module.
* **limitation** -- Instance of `Limitation <core_modules/comparator.module.html>`_ module.
* **random_seed** -- Random seed для инициализации random state, которые используется для генерации случайно выборки задач.

.. code-block:: python

   from core.impl import Optimize

    solution = Optimize(
        space: Space,
        logger: Logger,
        executor: Executor,
        instance: Instance,
        sampling: Sampling,
        function: Function,
        algorithm: Algorithm,
        comparator: Comparator,
        limitation: Limitation,
        random_seed: Optional[int]
    ).launch()

Estimate (abstract)
-------------------

| Данная абстракция позволяет вычислить значение фитнеса для конкретного `backdoor <instance_modules/variables.module.html#backdoor>`_.
| Estimation process зависит от следующих параметров:

* **space** -- Instance of `Space <core_modules/space.module.html>`_ module.
* **logger** -- Instance of Logger in `Output <output.html>`_ package.
* **executor** -- Instance of Executor in `Executor <executor.html>`_ package.
* **instance** -- Instance of Instance in `Instance <instance.html>`_ package. :)
* **sampling** -- Instance of `Sampling <core_modules/sampling.module.html>`_ module.
* **function** -- Instance of Function in `Function <function.html>`_ package.
* **comparator** -- Instance of `Comparator <core_modules/comparator.module.html>`_ module.
* **random_seed** -- Random seed для инициализации random state, который генерирует случайные сиды используемые для генерации выборок задач.

.. code-block:: python

   from core.impl import Estimate

    point = Estimate(
        space: Space,
        logger: Logger,
        instance: Instance,
        executor: Executor,
        sampling: Sampling,
        function: Function,
        comparator: Comparator,
        random_seed: Optional[int]
    ).estimate(backdoor)

Core models
-------------

.. toctree::
    :maxdepth: 1

    core_models/point.model

Core modules
-------------

.. toctree::
    :maxdepth: 1

    core_modules/space.module
    core_modules/sampling.module
    core_modules/comparator.module
    core_modules/limitation.module