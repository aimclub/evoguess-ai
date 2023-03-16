Sampling
========

| This module determines the sample size and is used to prepare chunk parameters for **worker_func** of `Function <../function.html>`_ implementations.

.. code-block:: python

    class Sampling:
        def max_chunks() -> int
        def get_state(offset: int, size: int) -> SamplingState

    class SamplingState:
        def chunks(results: Results) -> List[SampleChunk]

| The **get_state** method creates an instance of **SamplingState** with parameters **offset** and **size** for a specific estimating process.
| The **chunks** method returns a list of **SampleChunk** which depends on the size of the already computed **Results**. Each **SampleChunk** is a tuple of the form (**ChunkOffset**, **ChunkLength** ).

| You can also specify common arguments for all implementations:

* **split_into** -- Chunk size for one worker thread/process. To calculate the estimated value, the sample is split into **value/split_into** chunks.

Const sampling
--------------

This implementation defines a sample of constant **size**.

.. code-block:: python

    from core.module.sampling import Const

    sampling = Const(
        size: int,
        split_into: int
    )


Epsilon sampling
----------------

This implementation defines a sample of dynamic size, starting at **step_size** and gradually increasing to **max_size** in **step_size** increments.

.. code-block:: python

    from core.module.sampling import Epsilon

    sampling = Epsilon(
        step_size: int,
        epsilon: float,
        max_size: int,
        split_into: int,
        delta: float = 0.5
    )

Other core modules
------------------

* `Space <space.module.html>`_
* `Limitation <limitation.module.html>`_
* `Comparator <comparator.module.html>`_
