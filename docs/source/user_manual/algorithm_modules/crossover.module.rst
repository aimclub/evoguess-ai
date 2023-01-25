Crossover
=========

| In genetic algorithms, the crossover operator determines how two selected individuals will be crossed. Each individual is an instance of `Backdoor <../instance_modules/variables.module.html#backdoor>`_, and contains a bit mask that defines it. When crossing, the selected bits in the same positions are swapped and two new individuals are obtained at the output.

.. code-block:: python

    class Crossover:
        def cross(ind1: Backdoor, ind2: Backdoor) -> Tuple[Backdoor, Backdoor]

| The **cross** method returns a tuple of two new individuals, which is the result of applying the crossover operator to the passed **ind1** and **ind2**.

Uniform crossover
-----------------

When crossing, each pair of bits is swapped with a probability equal to **swap_prob**. The random number generator is initialized with the passed **random_seed**.

.. code-block:: python

   from algorithm.module.crossover import Uniform

    crossover = Uniform(
        swap_prob: float = 0.5,
        random_seed: Optional[int] = None
    )

One-point crossover
-------------------

When crossing, each pair of bits from **0** to **i** is swapped. The index **i** is randomly chosen in the range from **0** to the **length** of the bit mask. The random number generator is initialized with the passed **random_seed**.

.. code-block:: python

   from algorithm.module.crossover import OnePoint

    crossover = OnePoint(
        random_seed: Optional[int] = None
    )

Two-point crossover
-------------------

When crossing, each pair of bits from **i1** to **i2** is swapped. The index **i1** and **i2** are randomly chosen in the range from **0** to the **length** of the bit mask. The random number generator is initialized with the passed **random_seed**.

.. code-block:: python

   from algorithm.module.crossover import TwoPoint

    crossover = TwoPoint(
        random_seed: Optional[int] = None
    )


Other algorithm modules
-----------------------

* `Mutation <mutation.module.html>`_
* `Selection <selection.module.html>`_
