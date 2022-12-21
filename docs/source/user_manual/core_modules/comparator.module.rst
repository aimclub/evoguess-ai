Comparator
==========

This module describes the rules for comparing two objects.

.. code-block:: python

    class Comparator:
        def compare(obj1: Any, obj2: Any) -> int

MinValueMaxSize
---------------

To comparing two `points <../core_models/point.model.html>`_. Point with the minimum value will be selected. If the values are equal, the point with the maximum number of variables will be selected.

.. code-block:: python

    from core.module.comparator import MinValueMaxSize

    comparator = MinValueMaxSize()