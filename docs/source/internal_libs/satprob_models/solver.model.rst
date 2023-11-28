Solver Model
============

_Solver
-------

| Base interface for incremental solver instance with predefined ``formula`` and ``use_timer`` parameter.

.. note::
    To create an instance of this class use method `get_instance(...) <./solver.module.html#get_instance>`_.

.. function:: propagate(supplements)

        | This method makes propagation for given formula. First, all `Constraints <./variables.module.html#supplements>`_ from the passed ``supplements`` are substituted into the formula, then the `pysat.solvers.Solver.propagate(...) <https://pysathq.github.io/docs/html/api/solvers.html#pysat.solvers.Solver.propagate>`_ method is called with the list of `Assumptions <./variables.module.html#supplements>`_ from the passed ``supplements``.

    | Input arguments:

    * ``supplements`` (`Supplements <./variables.module.html#supplements>`_) - a formula supplements that are added while formula solving or propagating.

.. function:: solve(supplements, limit, extract_model)

        | This method solves given formula. First, `Constraints <./variables.module.html#supplements>`_ from the passed ``supplements`` are substituted into the formula, then the `pysat.solvers.Solver.solve(...) <https://pysathq.github.io/docs/html/api/solvers.html#pysat.solvers.Solver.propagate>`_ method is called with the list of `Assumptions <./variables.module.html#supplements>`_ from the passed ``supplements`` and resource ``limit``. The ``extract_model`` argument determines whether the satisfying assignment for the ``formula`` will be extracted from pysat solver.

    | Input arguments:

    * ``supplements`` (`Supplements <./variables.module.html#supplements>`_) - a formula supplements that are added while formula solving or propagating.

    * ``limit`` (Optional[`KeyLimit <../satprob_models/solver.model.html#KeyLimit>`_]) - a solving limit. Default: ``(None, 0)``.

    * ``extract_model`` (Optional[boolean]) - a flag to extract a satisfying assignment for the ``formula`` given to the solver. Default: ``True``.
