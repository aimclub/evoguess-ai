Point
=====

| This structure is used to represent specific points in the search `Space <../core_modules/space.module.html>`_ for `Algorithm <../algorithm.html>`_ during the optimization process. It contains a specific `Backdoor <../instance_modules/variables.module.html#backdoor>`_ and `Comparator <../core_modules/comparator.module.html>`_ rules. Each point can be assigned an appropriate fitness value (as part of the dictionary **estimation**).

.. code-block:: python

    class Point:
        def estimated() -> bool
        def value() -> Optional[float]
        def set(**estimation: Primitive) -> Point

| The **estimated** method method checks if a fitness value has been set and returns a boolean result.
| The **value** method returns *fitness value* or *None* if it hasn't already been set.
| The **set** method sets the fitness value and the information accompanying its calculation, and returns *self*.

The instance of **Point** class can be created like this:

.. code-block:: python

    from core.model.point import Point

    point = Point(
        backdoor: Backdoor,
        comparator: Comparator
    )


Vector
------

A type to represent a list of points for the optimization algorithm.

.. code-block:: python

    from core.model.point import Vector
    # it's only a type: Vector = List[Point]
