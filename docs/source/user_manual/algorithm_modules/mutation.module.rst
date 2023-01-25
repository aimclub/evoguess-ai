Mutation
========

| In evolution and genetic algorithms, the mutation operator determines how the original individuals will be mutated. Each individual is an instance of `Backdoor <../instance_modules/variables.module.html#backdoor>`_, and contains a bit mask that defines it. When mutating, the values of the selected bits in the mask are flipped.

.. code-block:: python

    class Mutation:
        def mutate(individual: Backdoor) -> Backdoor

| The **mutate** method returns a new individual, which is the result of applying the mutation operator to the passed **individual**.

Uniform mutation
----------------

When mutating, the value of each bit with a probability equal to **flip_scale/mask_length**  flips to the opposite, where **mask_length** is a length of bit mask. The random number generator is initialized with the passed **random_seed**.

.. code-block:: python

   from algorithm.module.mutation import Uniform

    selection = Uniform(
        flip_scale: float = 1.0,
        random_seed: Optional[Int] = None
    )

Doer mutation
-------------

См. статью (добавить ссылку позже).

.. code-block:: python

   from algorithm.module.mutation import Doer

    selection = Doer(
        beta: int = 3,
        random_seed: Optional[Int] = None
    )

Other algorithm modules
-----------------------

* `Crossover <crossover.module.html>`_
* `Selection <selection.module.html>`_
