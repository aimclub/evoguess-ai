Measure
=======

| This module defines evaluating measure of hardness and allows to set various limits. Both general methods of measure module uses in `Solver <solver.module.html>`_ implementations.

.. code-block:: python

    class Measure:
        def get_budget() -> Tuple[Optional[str], Optional[float]]:
        def check_and_get(stats: Dict[str, float], status: Optional[bool]) -> Tuple[Optional[float], Status]

| The **get_budget** method returns a string identifier of the selected measure with the value of **budget** argument passed during initialization, as a tuple.
| The **check_and_get** method selects the corresponding value of the selected measure from the passed **stats** dictionary and returns a tuple of this value and the option of **Status** enumerable type, which determines the resulting status of the processed task.

| You can also specify common arguments for all implementations:

* **budget** -- the *maximum* number of resources in the selected measure, that *can be* spent to solve one task instance.
* **at_least** -- the *minimum* number of resources in the selected measure, that *must be* spent to solve one task instance.

Solving time
------------

.. code-block:: python

    from function.module.measure import SolvingTime

    measure = SolvingTime(
        budget: Optional[float]
        at_least: Optional[float]
    )

Conflicts
---------

.. code-block:: python

    from function.module.measure import Conflicts

    measure = Conflicts(
        budget: Optional[float]
        at_least: Optional[float]
    )

Propagations
------------

.. code-block:: python

    from function.module.measure import Propagations

    measure = Propagations(
        budget: Optional[float]
        at_least: Optional[float]
    )

Learned literals
----------------

.. code-block:: python

    from function.module.measure import LearnedLiterals

    measure = LearnedLiterals(
        at_least: Optional[float]
    )

.. note::
    The **budget** argument of Learned literals measure doesn't support in available solvers!

Other function modules
----------------------

* `Solver <solver.module.html>`_
