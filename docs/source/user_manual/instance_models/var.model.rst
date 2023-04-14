Var
===

An interface for defining different types of variables and the logic to work with them.

.. code-block:: python

    Assumptions = List[int] # same as one lit Clauses
    Constraints = List[List[int]] # same as Clauses
    Supplements = Tuple[Assumptions, Constraints]

    AnyVar = Union[Var, int]
    VarMap = Dict[AnyVar, int]

    class Var:
        def deps() -> List[AnyVar]
        def supplements(var_map: VarMap) -> Supplements

.. note::
    The Var also has implementations of methods __str__, __hash__ and __eq__.

Index
------

Implementation for creating a boolean variable.

.. code-block:: python

    from instance.module.variables.vars import Index

    var = Index(index: int)

Domain
------

Implementation for creating a virtual domain variable with **name**. The domain is determined by the size of the list of dependent boolean variables **group**.

.. code-block:: python

    from instance.module.variables.vars import Domain

    var = Domain(name: str, group: List[int])

Switch
------

Implementation for creating a virtual toggle variable with **name**. The value of such a variable is determined by the result of calling the boolean function **fn** on the set of values from dependent boolean variables **group**.

.. code-block:: python

    from instance.module.variables.vars import Switch

    var = Switch(name: str, group: List[int], fn: Callable)

XorSwitch
---------

Implementation of Switch variable with predefined function **fn** as xor.

.. code-block:: python

    from instance.module.variables.vars import XorSwitch

    var = Switch(name: str, group: List[int])

MajoritySwitch
--------------

Implementation of Switch variable with predefined function **fn** as majority.

.. code-block:: python

    from instance.module.variables.vars import MajoritySwitch

    var = MajoritySwitch(name: str, group: List[int])

Bent4Switch
-----------

Implementation of Switch variable with predefined function **fn** as bent4.

.. code-block:: python

    from instance.module.variables.vars import Bent4Switch

    var = Bent4Switch(name: str, group: List[int])

