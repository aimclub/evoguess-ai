Space
=====

.. code-block:: python

    class Space:
        def get_initial(instance: Instance) -> Backdoor


Input set space
---------------

.. code-block:: python

    from core.module.space import InputSet

    space = InputSet(
        by_mask: Mask = None,
        by_string: str = None
    )

Search set space
----------------

.. code-block:: python

    from core.module.space import SearchSet

    space = SearchSet(
        variables: Variables,
        by_mask: Mask = None,
        by_string: str = None
    )
