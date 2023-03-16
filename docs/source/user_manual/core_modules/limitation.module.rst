Limitation
==========

| This module defines the resource limits that are used by the `Algorithm <../algorithm.html>`_ during the optimization process.

.. code-block:: python

    class Limitation:
        def exhausted() -> bool:
        def left(key: str) -> Optional[Numeral]
        def set(key: str, value: Numeral) -> Numeral
        def get(key: str, default: Numeral) -> Numeral
        def increase(key: str, value: Numeral) -> Numeral

| The **exhausted** method checks if the selected resource has been exhausted and returns a boolean result.
| The **left** method returns the remaining limit for the **key** resource.
| The **set** method updates the **key** resource with the given **value** and returns the updated value.
| The **get** method returns the current value for the **key** resource. If the **key** resource is missing, then returns the **default** value.
| The **increase** method adds **value** to the current value of the **key** resource and returns the updated value.

WallTime
--------

This implementation uses execution time as the selected resource. The execution time is limited by the **from_string** parameter in the *'<hours>:<minutes>:<seconds>'* format.

.. code-block:: python

    from core.module.limitation import WallTime

    limitation = WallTime(
        from_string: str
    )

Iteration
---------

This implementation uses iterations as the selected resource. The number of iterations is limited using the **value** parameter.

.. code-block:: python

    from core.module.limitation import Iteration

    limitation = Iteration(
        value: int
    )

Other core modules
------------------

* `Space <space.module.html>`_
* `Sampling <sampling.module.html>`_
* `Comparator <comparator.module.html>`_
