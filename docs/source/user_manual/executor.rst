Executor
========

This package is used to manage tasks in multithreaded and distributed computing environments.

Thread Executor
---------------

| Implementation using the standard `ThreadPoolExecutor <https://docs.python.org/3/library/concurrent.futures.html>`_. The **max_workers** parameter specifies the maximum number of threads to be created. Its default value `os.cpu_count <https://docs.python.org/3/library/os.html>`_.

.. code-block:: python

    from executor.impl import ThreadExecutor

    executor = ThreadExecutor(
        max_workers: Optional[int]
    )

Process Executor
----------------

| Implementation using the standard `ProcessPoolExecutor <https://docs.python.org/3/library/concurrent.futures.html>`_. The **max_workers** parameter specifies the maximum number of processes to be created. Its default value `os.cpu_count <https://docs.python.org/3/library/os.html>`_.

.. code-block:: python

    from executor.impl import ProcessExecutor

    executor = ProcessExecutor(
        max_workers: Optional[int]
    )

MPI Executor
------------

| Implementation for distributed computing through Message Passing Interface (MPI) using the `MPIPoolExecutor <https://mpi4py.readthedocs.io/en/stable/mpi4py.futures.html#mpipoolexecutor>`_ from `mpi4py <https://pypi.org/project/mpi4py/>`_ library. Automatically determines the number of resources that were allocated at startup.

.. code-block:: python

    from executor.impl import MPIExecutor

    executor = MPIExecutor()

