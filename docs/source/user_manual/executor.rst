Executor
========

This package is used для распределения задач в многопоточных и распределенных вычислительных среда.

Thread Executor
---------------

Реализация c использованием стандартного `ThreadPoolExecutor <https://docs.python.org/3/library/concurrent.futures.html>`_. Параметр **max_workers** определяет максимальное число потоков, которое будет создано. По умолчанию равно `os.cpu_count <https://docs.python.org/3/library/os.html>`_.

.. code-block:: python

    from executor.impl import ThreadExecutor

    executor = ThreadExecutor(
        max_workers: Optional[int]
    )

Process Executor
----------------

Реализация c использованием стандартного `ProcessPoolExecutor <https://docs.python.org/3/library/concurrent.futures.html>`_. Параметр **max_workers** определяет максимальное число процессов, которое будет создано. По умолчанию равно `os.cpu_count <https://docs.python.org/3/library/os.html>`_.

.. code-block:: python

    from executor.impl import ProcessExecutor

    executor = ProcessExecutor(
        max_workers: Optional[int]
    )

MPI Executor
------------

Реализация для распределенных вычислений посредством MPI. Автоматически определяет число ресурсов, которые были выделены при запуске.

.. code-block:: python

    from executor.impl import MPIExecutor

    executor = MPIExecutor()

