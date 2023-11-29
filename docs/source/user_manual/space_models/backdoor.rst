Backdoor
--------

| An implementation to create a custom set of variables that is used as a backdoor model in optimization `algorithms <../../algorithm.html>`_. This implementation can quickly define subsets of the original set of variables using bit masks. Each variable in the original set can be either "on" or "off" at the same time. The "on" variables form the required subset of variables.

| The instance of **Backdoor** is specified via the **from_file** or **from_vars** arguments, similar to the **Variables** implementation.

.. note::
    Backdoors automatically built in `Space <../core_modules/space.module.html>`_ module from user-selected variables.

.. code-block:: none

    from lib_satprob.variables import Backdoor

    backdoor = Backdoor(
        from_file: str,
        from_vars: List[Var]
    )