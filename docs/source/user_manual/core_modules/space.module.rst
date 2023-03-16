Space
=====

| This module defines the search space for the `Algorithm <../algorithm.html>`_. During the optimization process, the algorithm will use only variables from the list specified during initialization.

.. code-block:: python

    class Space:
        def get_initial(instance: Instance) -> Backdoor

The **get_initial** method returns a backdoor that contains all search space variables, which can be in one of two states: 'on' or 'off' depending on the specified **by_mask** or **by_string** filter. By default, if no filters are passed, all variables are 'on'. Only **one** of the following filters can be used during initialization:

* **by_mask** -- List of bit values. The returned backdoor will include variables whose indexes contain positive bits.
* **by_string** -- List of variable names to be included in the returned backdoor.

Search set space
----------------

The search space is specified by a set of **variables** as instance of `Variables <../instance_modules/variables.module.html>`_ module.

.. code-block:: python

    from core.module.space import SearchSet

    space = SearchSet(
        variables: Variables,
        by_mask: Mask = None,
        by_string: str = None
    )

Input set space
---------------

The search space is specified by a set of variables contained in the **input_set** argument of the `StreamCipher <../instance.html#stream-cipher>`_ instance, which is passed as an argument to the **get_initial** method.

.. code-block:: python

    from core.module.space import InputSet

    space = InputSet(
        by_mask: Mask = None,
        by_string: str = None
    )

Rho subset space
----------------

The search space is specified by a set of **variables** as instance of `Variables <../instance_modules/variables.module.html>`_ module, from which **of_size** are chosen as priorities.

.. code-block:: python

    from core.module.space import RhoSubset

    space = RhoSubset(
        of_size: int,
        variables: Variables,
        by_mask: Mask = None,
        by_string: str = None
    )

Other core modules
------------------

* `Sampling <sampling.module.html>`_
* `Limitation <limitation.module.html>`_
* `Comparator <comparator.module.html>`_
