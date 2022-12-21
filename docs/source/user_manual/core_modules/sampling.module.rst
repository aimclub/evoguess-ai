Sampling
========

This module determines the sample size and is used to prepare chunk parameters for **worker_func** of `Function <../function.html>`_. Метод **get_state(...)** создает экземпляр **SamplingState** с параметрами **offset** and **size** для конкретного процесса оценки. Метод **chunks(...)** возвращает список из **SampleChunk**, размер которого зависит от уже полученных **Results**. Каждый **SampleChunk** имеет формат (**ChunkOffset**, **ChunkLength**).

.. code-block:: python

    class Sampling:
        def max_chunks() -> int
        def get_state(offset: int, size: int) -> SamplingState

    class SamplingState:
        def chunks(results: Results) -> List[SampleChunk]

Const sampling
--------------

This implementation defines a sample of constant **size**. During the estimation, the selection will be split into **value/split_into** chunks of size equals to **split_into**.

.. code-block:: python

    from core.module.sampling import Const

    sampling = Sampling(
        size: int,
        split_into: int
    )


Epsilon sampling
----------------

.. code-block:: python

    from core.module.sampling import Epsilon

    sampling = Epsilon(
        step_size: int,
        epsilon: float,
        max_size: int,
        split_into: int,
        delta: float = 0.5
    )
