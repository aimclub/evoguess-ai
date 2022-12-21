Measure
=======

Measure of hardness.

Solving time
------------

.. code-block:: python

    measure = SolvingTime(
        budget: Optional[float]
        at_least: Optional[float]
    )

Conflicts
---------

.. code-block:: python

    measure = Conflicts(
        budget: Optional[float]
        at_least: Optional[float]
    )

Propagations
------------

.. code-block:: python

    measure = Propagations(
        budget: Optional[float]
        at_least: Optional[float]
    )

Learned literals
----------------

.. code-block:: python

    measure = LearnedLiterals(
        budget: Optional[float]
        at_least: Optional[float]
    )

