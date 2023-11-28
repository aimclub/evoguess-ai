Solver Module
=============

| This module for solving task instances of some `Problem <../lib_satprob.html#problem>`_ that arise when substituting specific values of `Variables <./variables.module.html#variables>`_ that are presented in the `Encoding <./encoding.module.html#encoding>`_.

Solver
------

| Module interface for defining the `Problem <../lib_satprob.html#problem>`_ solving tool. It has one inherited method: `get_instance(...) <#get_instance>`_, which should return an instance of `_Solver <../satprob_models/solver.model.html#_solver>`_.

.. code-block:: python

    class lib_satprob.solver.Solver()

| Base **Solver** class constructor haven't any arguments.

Report
^^^^^^

| A structure for representing the solver's output and associated statistics.

.. code-block:: python

    class lib_satprob.solver.Report(
        status: Optional[bool]
        stats: Dict[str, float]
        model: List[int]
        cost: int
    )

KeyLimit
^^^^^^^^

| An tuple to limit the solver's process resources for one run.

.. code-block:: python

    type lib_satprob.solver.KeyLimit = Tuple[str, float]

Example:

.. code-block:: python

    time_limit = ('time', 5) # 5 seconds
    conflicts_limit = ('conflicts', 1000) # 1000 conflicts
    propagations_limit = ('propagations', 1000) # 1000 propagations

Solver Methods
^^^^^^^^^^^^^^

.. function:: get_instance(formula, use_timer)

    | This method creates an instance of solver for given ``formula``. Created solver instance allows to **propagate** or **solve** a given ``formula`` multiple times on different `Supplements <./variables.module.html#supplements>`_ without reinitialising the wrapped solver.

    .. note::

        Currently, reinitialising is skipped only if the ``formula`` is a `pysat.formula.CNF <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.CNF>`_ instance (that is, the encoding is `CNF <./encoding.module.html#cnf>`_ or `CNFPlus <./encoding.module.html#cnfplus>`_ instance) instance and the passed ``supplements`` contains only an `Assumptions <./variables.module.html#supplements>`_ part.

    | Input arguments:

    * ``formula`` (`Formula <./encoding.module.html#formula>`_) - a encoding formula returned by `Encoding.get_formula(...) <./encoding.module.html#get_formula>`_ method.

    * ``use_timer`` (Optional[boolean]) - a flag to enable timer while solving. If timer disabled then resulting `Report <#report>`_ doesn't contain time value in **stats** dictionary. Default: ``True``.

    | Return type: `_Solver <../satprob_models/solver.model.html#_solver>`_

.. function:: propagate(formula, supplements, use_timer)

    | This method makes propagation for given formula. First, all `Constraints <./variables.module.html#supplements>`_ from the passed ``supplements`` are substituted into the formula, then the `pysat.solvers.Solver.propagate(...) <https://pysathq.github.io/docs/html/api/solvers.html#pysat.solvers.Solver.propagate>`_ method is called with the list of `Assumptions <./variables.module.html#supplements>`_ from the passed ``supplements``.

    .. note::

        The method `Solver.propagate(...) <#propagate>`_ works only for `CNF <./encoding.module.html#cnf>`_ or `CNFPlus <./encoding.module.html#cnfplus>`_ encodings (that is, for SAT problems specified by the implementation of `SatProblem <../lib_satprob.html#satproblem>`_).

    | Input arguments:

    * ``formula`` (`Formula <./encoding.module.html#formula>`_) - a encoding formula returned by `Encoding.get_formula(...) <./encoding.module.html#get_formula>`_ method.

    * ``supplements`` (`Supplements <./variables.module.html#supplements>`_) - a formula supplements that are added while formula solving or propagating.

    * ``use_timer`` (Optional[boolean]) - a flag to enable timer while solving. If timer disabled then resulting `Report <#report>`_ doesn't contain time value in **stats** dictionary. Default: ``True``.

    | Return type: `Report <#report>`_

.. function:: solve(formula, supplements, limit, extract_model, use_timer)

    | This method solves given formula. First, `Constraints <./variables.module.html#supplements>`_ from the passed ``supplements`` are substituted into the formula, then the `pysat.solvers.Solver.solve(...) <https://pysathq.github.io/docs/html/api/solvers.html#pysat.solvers.Solver.propagate>`_ method is called with the list of `Assumptions <./variables.module.html#supplements>`_ from the passed ``supplements`` and resource ``limit``. The ``extract_model`` argument determines whether the satisfying assignment for the ``formula`` will be extracted from pysat solver.

    | Input arguments:

    * ``formula`` (`Formula <./encoding.module.html#formula>`_) - a encoding formula returned by `Encoding.get_formula(...) <./encoding.module.html#get_formula>`_ method.

    * ``supplements`` (`Supplements <./variables.module.html#supplements>`_) - a formula supplements that are added while formula solving or propagating.

    * ``limit`` (Optional[`KeyLimit <../satprob_models/solver.model.html#KeyLimit>`_]) - a solving limit. Default: ``(None, 0)``.

    * ``extract_model`` (Optional[boolean]) - a flag to extract a satisfying assignment for the ``formula`` given to the solver. Default: ``True``.

    * ``use_timer`` (Optional[boolean]) - a flag to enable timer while solving. If timer disabled then resulting `Report <#report>`_ doesn't contain time value in **stats** dictionary. Default: ``True``.

    | Return type: `Report <#report>`_

PySatSolver
-----------

| Implementation for pysat solver. ... about lib

.. code-block:: python

    class lib_satprob.solver.PySatSolver(sat_name='m22': str, max_sat_alg='rc2': str)

| Init arguments:

* ``sat_name`` (Optional[str]) - argument specifies ...

* ``max_sat_alg`` (Optional[str]) - argument specifies ...

| This implementation может использоваться для решения SAT and MaxSAT проблем.
