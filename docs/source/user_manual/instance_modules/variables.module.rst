Variables
=========

| This module is used to provide information about sets of variables that are present in the `Encoding <./encoding.module.html>`_ of the problem under study. Sets can simultaneously include different types of supported variables, such as: `Index <../instance_models/var.model.html#index>`_, `Switch <../instance_models/var.model.html#switch>`_ or `Domain <../instance_models/var.model.html#domain>`_ variables.

.. code-block:: python

    AnyVar = Union[Var, int]

    class Variables:
        def variables() -> List[Var]
        def get_var_deps() -> Iterable[AnyVar]
        def get_var_bases() -> List[int]
        def get_deps_bases() -> List[int]

.. note::
    The Variables also has implementations of methods __len__, __contains__, __iter__, __hash__, __eq__, __repr__ and __str__.

Variables
---------

The instance of **Variables** can either be created by reading from a file, or given directly via a list of variables. Only **one** of the following arguments can be used during initialization:

* **from_file** -- Path to a file that contains a list of variables in JSON format.
* **from_vars** -- A list of variables that implement `Var <../instance_models/var.model.html>`_ abstract class.

.. code-block:: python

    from instance.module.variables import Variables

    variables = Variables(
        from_file: str,
        from_vars: List[Var]
    )

Variables examples
^^^^^^^^^^^^^^^^^^

1) A list of `Index <../instance_models/var.model.html#index>`_ boolean variables from 1 to 64 inclusive.

.. code-block:: python

    from instance.module.variables import Variables
    from instance.module.variables.vars import Index

    variables = Variables(from_vars=[Index(i) for i in range(1, 65)])

2) A list of 4 `Domain <../instance_models/var.model.html#domain>`_ variables with domain size 5. Each domain variable is defined with 5 boolean variables.

.. code-block:: python

    from instance.module.variables import Variables
    from instance.module.variables.vars import Domain

    variables = Variables(from_vars=[
        Domain('d1', [1, 2, 3, 4, 5]), Domain('d2', [6, 7, 8, 9, 10]),
        Domain('d3', [11, 12, 13, 14, 15]), Domain('d4', [16, 17, 18, 19, 20])
    ])

2) A list of 26 (from 1 to 25 inclusive and under index 28) boolean variables and 3 `Switch <../instance_models/var.model.html#switch>`_ variables over the XOR operator.

.. code-block:: python

    from instance.module.variables import Variables
    from instance.module.variables.vars import Index, XorSwitch

    variables = Variables(from_vars=[
        *(Index(i) for i in range(1, 26)), XorSwitch('x1', [26, 27]),
        Index(28), XorSwitch('x2', [29, 30]), XorSwitch('x3', [31, 32])
    ])

Indexes
-------

Implementation for creating multiple variables using their numbers in the `Encoding <./encoding.module.html>`_. Variable numbers can be specified either as a string via the **from_string** argument, or via the **from_iterable** argument using any Python iterable object.

.. note::
    Creation via **from_string** argument also supports internal intervals, for example: '1 2 3..8 10'

.. code-block:: python

    from instance.module.variables import Indexes

    variables = Indexes(
        from_string: str,
        from_iterable: Iterable[int],
    )

Indexes examples
^^^^^^^^^^^^^^^^

.. note::
    If the list of variables contains only `Index <../instance_models/var.model.html#index>`_ boolean variables, then it is more convenient to define such sets using the **Indexes** implementation.

Various ways to define lists of boolean variables using only their numbers.

.. code-block:: python

    from instance.module.variables import Indexes

    variables = Indexes(from_string='1..24')
    # or
    variables = Indexes(from_iterable=range(1, 25))

    variables = Indexes(from_string='1 3 6 10')
    # or
    variables = Indexes(from_iterable=[1 3 6 10])

    variables = Indexes(from_string='1..5 12 15 23..25')
    # or
    variables = Indexes(from_iterable=[1, 2, 3, 4, 5, 12, 15, 23, 24, 25])
    # or
    variables = Indexes(from_iterable=[*range(1, 6), 12, 15, *range(23, 26)])

Interval
--------

Implementation for creating a set of variables that are contained in the interval from **start** with length **length**. Or you can specify the interval as a string **'<start>..<end>'** (including **end**) via the **from_string** argument.

.. code-block:: python

    from instance.module.variables import Interval

    variables = Interval(
        start: int,
        length: int,
        from_string: str
    )

Interval examples
^^^^^^^^^^^^^^^^^

Various ways to define interval of boolean variables.

.. code-block:: python

    from instance.module.variables import Interval

    variables = Interval(start=1, length=64)
    # or
    variables = Interval(from_string='1..64')
    # the same as
    variables = Indexes(from_iterable=range(1, 65))
    # or
    variables = Indexes(from_string='1..64')

Backdoor
--------

| An implementation to create a custom set of variables that is used as a backdoor model in optimization `algorithms <../algorithm.html>`_. This implementation can quickly define subsets of the original set of variables using bit masks. Each variable in the original set can be either "on" or "off" at the same time. The "on" variables form the required subset of variables.

| The instance of **Backdoor** is specified via the **from_file** or **from_vars** arguments, similar to the **Variables** implementation.

.. note::
    Backdoors automatically built in `Space <../core_modules/space.module.html>`_ module from user-selected variables.

.. code-block:: none

    from instance.module.variables import Backdoor

    backdoor = Backdoor(
        from_file: str,
        from_vars: List[Var]
    )

Other instance modules
----------------------

* `Encoding <encoding.module.html>`_
