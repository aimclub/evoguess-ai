Variables Module
================

| This module for providing information about sets of variables that are presented in the `Encoding <./encoding.module.html#encoding>`_ of some `Problem <../lib_satprob.html#problem>`_. Sets can simultaneously include different types of supported variables, such as: `Index <../satprob_models/var.model.html#index>`_, `Switch <../satprob_models/var.model.html#switch>`_ or `Domain <../satprob_models/var.model.html#domain>`_ variables.

Variables
---------

| Base module class for creating a set of variables.

.. code-block:: python

    class lib_satprob.variables.Variables(
        from_file: str,
        from_vars: List[Var]
    )

| Init arguments:

* ``from_file`` (Optional[str]) - a path to the file containing a JSON object with a list variables. This argument involves lazily creation by reading from the given file. Default: ``None``.

* ``from_vars`` (List[`Var <../satprob_models/var.model.html#var>`_]) - a list of variables that implement `Var <../satprob_models/var.model.html#var>`_ abstract class.

.. important::
    To create a `Variables <#variables>`_ instance specify only one initialization argument (``from_file`` **or** ``from_vars``).

Supplements
^^^^^^^^^^^

| Some substitution into the source encoding, which consists of variable values in **Assumptions** and additional **Constraints**.

.. code-block:: python

    type lib_satprob.variables.Assumptions = List[int]
    type lib_satprob.variables.Constraints = List[List[int]]
    type lib_satprob.variables.Supplements = Tuple[Assumptions, Constraints]

Variables Methods
^^^^^^^^^^^^^^^^^

.. function:: variables()

    | This method returns a list of contained variables.

    | Return type: List[`Var <../satprob_models/var.model.html#var>`_]

.. function:: dimension()

    | This method returns a list of integers. Each integer represents the number of possible values that the corresponding variable can take. Essentially, this is a list of values `Var.dim <../satprob_models/var.model.html#dim>`_ for each contained variable.

    | Return type: List[int]

.. function:: power()

    | This method returns a the number of all possible unique `Supplements <#supplements>`_ that can be obtained for a given list of variables. Essentially, this is the product of a list of numbers that the `Variables.dimension() <#dimension>`_ method returns.

    | Returns type: int

.. function:: substitute(using_values, using_var_map)

    | This method substitutes values into each contained variable using the `Var.substitute(...) <../satprob_models/var.model.html#substitute>`_ method, and returns the combined result of their calls.

    | Input arguments:

    * ``using_values`` (Optional[List[int]]) - a list of numbers in range of ``0`` to `Variables.dimension() <#dimension>`_ for each contained variable.

    * ``using_var_map`` (Optional[`VarMap <satprob_models/var.model.html#varmap>`_]) - a dictionary where each contained variable is associated with a number in range of ``0`` to `Var.dim <../satprob_models/var.model.html#dim>`_.

    .. important::

        To substitute values specify only one input argument (``using_values`` **or** ``using_var_map``).

    | Return type: `Supplements <#supplements>`_

.. function:: enumerate(offset, length, with_random_state)

    | This method enumerates all possible unique `Supplements <#supplements>`_ for a given list of variables starting with `Supplements <#supplements>`_ obtained by substituting the values ``{ 0 }^n`` and ending with the maximum values for the corresponding `Variables.dimension() <#dimension>`_ (for example ``{ 1 }^n`` if all variables are binary), where ``n`` is equal to the length of there `Variables.dimension() <#dimension>`_.

    | The method provides from `Enumerable.enumerate(...) <satprob_models/enumerable.model.html#enumerate>`_ inherited class.

    | Input arguments:

    * ``offset`` (Optional[int]) - a count of leading `Supplements <#supplements>`_ that will be skipped. Default: ``0``.

    * ``length`` (Optional[int]) - a count of `Supplements <#supplements>`_ that will be returned. If equals ``None`` then return all `Supplements <#supplements>`_ from ``offset`` to end. Default: ``None``.

    * ``with_random_state`` (Optional[`RandomState <https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState>`_]) - a state that is used to shuffle order of returned `Supplements <#supplements>`_. If equals ``None`` then returns in usual order. Default: ``None``.

    | Return type: List[`Supplements <#supplements>`_]

| Example (1): A list of `Index <../satprob_models/var.model.html#index>`_ Boolean variables from **1** to **4** inclusive.

.. code-block:: python

    >>> from lib_satprob.variables import Variables
    >>> from lib_satprob.variables.vars import Index
    >>> vars = [Index(i) for i in range(1, 5)]
    >>> variables = Variables(from_vars=vars)
    >>> print(variables)
    [Index(1), Index(2), Index(3), Index(4)]

| Example (2): A list of four `Domain <../satprob_models/var.model.html#domain>`_ variables with domain size (`Var.dim <../satprob_models/var.model.html#dim>`_) of 5. Each domain variable is defined over five Boolean variables.

.. code-block:: python

    >>> from lib_satprob.variables import Variables
    >>> from lib_satprob.variables.vars import Domain
    >>> vars = [
    >>>     Domain('d1', [1, 2, 3, 4, 5]),
    >>>     Domain('d2', [6, 7, 8, 9, 10]),
    >>>     Domain('d3', [11, 12, 13, 14, 15]),
    >>>     Domain('d4', [16, 17, 18, 19, 20])
    >>> ]
    >>> variables = Variables(from_vars=vars)
    >>> print(variables)
    [Domain('d1'), Domain('d2'), Domain('d3'), Domain('d4')]

| Example (3): A list of four (from **1** to **3** inclusive and with index **6**) Boolean variables and one `Switch <../satprob_models/var.model.html#switch>`_ variable over XOR operator.

.. code-block:: python

    >>> from lib_satprob.variables import Variables
    >>> from lib_satprob.variables.vars import Index, XorSwitch
    >>> vars = [
    >>>     *(Index(i) for i in range(1, 4)),
    >>>     XorSwitch('x1', [4, 5]),
    >>>     Index(6),
    >>> ]
    >>> variables = Variables(from_vars=vars)
    >>> print(variables)
    [Index(1), Index(2), Index(3), XorSwitch('x1'), Index(6)]

Indexes
-------

| Module implementation for creating a set of Boolean `Index <../satprob_models/var.model.html#index>`_ variables by their indexes, which are contained in the `Encoding <./encoding.module.html#encoding>`_ formula.

.. code-block:: python

    class lib_satprob.variables.Indexes(
        from_string: str,
        from_iterable: Iterable[int]
    )

| Init arguments:

* ``from_string`` (Optional[str]) - a string with space-separated indexes of the corresponding variables. Default: ``None``.

* ``from_iterable`` (Optional[List[int]]) - a list of integer indexes of the corresponding variables. Default: ``None``.

.. important::

    To create an `Indexes <variables.module.html#indexes>`_ instance specify only one initialization argument (``from_string`` **or** ``from_iterable``). Creation via ``from_string`` argument also supports internal intervals, for example: ``'1 2 3..8 10'``

| Examples:

.. code-block:: python

    >>> from lib_satprob.variables import Indexes
    >>> variables = Indexes(from_string='1 3..5 8')
    >>> print(variables)
    [Index(1), Index(3), Index(4), Index(5), Index(8)]

.. code-block:: python

    >>> from lib_satprob.variables import Interval
    >>> variables = Range(from_iterable=[1, 3, 4, 8])
    >>> print(variables)
    [Index(1), Index(3), Index(4), Index(8)]

Range
-----

| Module implementation for creating a set of Boolean `Index <../satprob_models/var.model.html#index>`_ variables in the range from **start** index and containing **length** indices in overall.

.. code-block:: python

    class lib_satprob.variables.Range(
        start: int,
        length: int
    )

| Init arguments:

*  ``start`` (int) - a start variable index of the range.

*  ``length`` (int) - a number of indices in the range.

| Example:

.. code-block:: python

    >>> from lib_satprob.variables import Range
    >>> variables = Range(start=1, length=4)
    >>> print(variables)
    [Index(1), Index(2), Index(3), Index(4)]
