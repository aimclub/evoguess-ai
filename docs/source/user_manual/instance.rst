Instance
========

Данный пакет предназначен для представления модели решаемой проблемы.

Instance
--------

Реализация для представления модели задачи только посредством кодировки задачи. Используется если внутренняя структура переменных либо не известна, либо не нужна для решения поставленной задачи.

| Определяющие параметры:

* **encoding** -- Instance of `Encoding <instance_modules/encoding.module.html>`_ module.

.. code-block:: python

    from instance.impl import Instance

    instance = Instance(
        encoding: Encoding
    )

Stream Cipher
-------------

Реализация для представления модели задачи, для которой известно множество входных или выходных переменных. Предполагается использование для работы с задачами обращения различных функций. Также можно указать дополнительное множество переменных для ослабления кодировки, означивание литералов для которых будет также выполнено в процессе построения задачи обращения.

| Определяющие параметры:

* **encoding** -- Instance of `Encoding <instance_modules/encoding.module.html>`_ module.
* **input_set** -- Instance of `Variables <instance_modules/variables.module.html>`_ module.
* **output_set** -- Instance of Indexes in `Variables <instance_modules/variables.module.html>`_ module.
* **extra_set** -- Optional instance of `Variables <instance_modules/variables.module.html>`_ module.

.. code-block:: python

    from instance.impl import StreamCipher

    instance = StreamCipher(
        encoding: Encoding,
        input_set: Indexes,
        output_set: Variables,
        extra_set: Optional[Variables]
    )

Instance modules
----------------

.. toctree::
    :maxdepth: 1

    instance_modules/encoding.module
    instance_modules/variables.module