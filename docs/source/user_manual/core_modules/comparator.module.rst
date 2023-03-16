Comparator
==========

| This module describes the rules for comparing two **Ordered** objects.

.. code-block:: python

    class Ordered:
        def __init__(comparator: Comparator)

    class Comparator:
        def compare(obj1: Ordered, obj2: Ordered) -> int

| The **compare** method returns the comparison result for **obj1** and **obj2**.

.. note::
    This method is used for special method realisations __lt__, __le__, __eq__, __gt__, __ge__ in class **Ordered**.

MinValueMaxSize
---------------

This implementation compares two `Points <../core_models/point.model.html>`_. Point with the minimum value will be selected. If the values are equal, the point with the maximum number of variables will be selected.

.. code-block:: python

    from core.module.comparator import MinValueMaxSize

    comparator = MinValueMaxSize()

Other core modules
------------------

* `Space <space.module.html>`_
* `Sampling <sampling.module.html>`_
* `Limitation <limitation.module.html>`_
