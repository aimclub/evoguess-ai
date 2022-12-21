Limitation
==========

Limits the resources used by algorithms in the optimization process.

.. code-block:: python

    class Limitation:
        def exhausted() -> bool:
        def left(key: str) -> Optional[Numeral]
        def set(key: str, value: Numeral) -> Numeral
        def get(key: str, default: Numeral) -> Numeral
        def increase(key: str, value: Numeral) -> Numeral

WallTime
--------

Limits execution time. *from_string* format: '<hours>:<minutes>:<seconds>'.

.. code-block:: python

    from core.module.limitation import WallTime

    limitation = WallTime(
        from_string: str
    )

Iteration
---------

Limits the number of algorithm iterations.

.. code-block:: python

    from core.module.limitation import Iteration

    limitation = Iteration(
        value: int
    )
