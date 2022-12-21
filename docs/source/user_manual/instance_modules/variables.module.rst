Variables
=========

Модуль для указания множества переменных. Множество переменных можно либо считать из файла, указав к нему путь через аргумент **from_file**, либо задать напрямую через аргумент **from_vars**. Этот аргумент принимает список объектных переменных реализующих интерфейс `Var <var.implementation.html>`_.

.. code-block:: python

    from instance.module.variables import Variables

    variables = Variables(
        from_file: str,
        from_vars: List[Var]
    )

Indexes
-------

Реализация для создания множества переменных, используя их номера в исходной кодировке. Номера переменных можно указать либо в виде строки через аргумент **from_string**, либо через аргумент **from_iterable** с помощью любой Iterable структуры языка python.

.. note::
    Создание через параметр **from_string** также поддерживает внутренние интервалы, например: '1 2 3..8 10'

.. code-block:: python

    from instance.module.variables import Indexes

    variables = Indexes(
        from_string: str,
        from_iterable: Iterable[int],
    )

Interval
--------

Реализация для создания множества переменных, через интервал с их номерами, начало которого задается через аргумент **start**, а длина через аргумент **length**. Либо можно задать интервал в виде строки **'<start>..<end>'** (including **end**) через аргумент **from_string**.

.. code-block:: python

    from instance.module.variables import Interval

    variables = Interval(
        start: int,
        length: int,
        from_string: str
    )

Backdoor
--------

| Реализация для создания специального множества переменных, которое используется в качестве модели лазеек в алгоритмах оптимизации. Позволяет быстро определять подмножества исходного множества переменных посредством битовых масок. Каждая переменная в исходном множестве может быть одновременно либо "включена", либо "выключена". "Включенные" переменные образуют требуемое подмножество переменных.
| Также, как и реализация **Variables**, может задаваться через аргументы **from_file** или **from_vars**.

.. note::
    Backdoors automatically built in `Space <../core_modules/space.module.html>`_ module from user-selected variables.

.. code-block:: none

    from instance.module.variables import Backdoor

    backdoor = Backdoor(
        from_file: str,
        from_vars: List[Var]
    )

Examples
--------

1) Множество переменных как интервал [1, 64].

.. code-block:: python

    from instance.module.variables import Interval

    variables = Interval(start=1, length=64)
    # or
    variables = Interval(from_string='1..64')

2) Множество переменных, используя их номера.

.. code-block:: python

    from instance.module.variables import Indexes

    variables = Indexes(from_string='1..24')
    # or
    variables = Indexes(from_iterable=range(1, 25))

    variables = Indexes(from_string='1..5 12 15 23..25')
    # or
    variables = Indexes(from_iterable=[1, 2, 3, 4, 5, 12, 15, 23, 24, 25])
    # or
    variables = Indexes(from_iterable=[*range(1, 6), 12, 15, *range(23, 26)])

3) Множество переменных, используя реализации `Var <var.implementation.html>`_.

.. code-block:: python

    from instance.module.variables import Indexes
    from instance.module.variables import Variables
    from instance.module.variables.vars import Index, XorSwitch

    variables = Indexes(from_iterable=range(1, 25))
    # or
    variables = Variables(from_vars=[Index(i) for i in range(1, 25)])

    variables = Variables(from_vars=[
        *(Index(i) for i in range(1, 26)), XorSwitch('x1', [26, 27]),
        Index(28), XorSwitch('x2', [29, 30]), XorSwitch('x3', [31, 32])
    ])


.. toctree::
    :maxdepth: 1
    :caption: About Var

    var.implementation