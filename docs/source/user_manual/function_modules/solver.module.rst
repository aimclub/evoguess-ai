Solver
=======

| This module defines the tools for task solving. Tasks are represented using `Encoding <../instance_modules/encoding.module.html>`_ implementations.

.. code-block:: python

    class IncrSolver:
        def solve(assumptions: Assumptions) -> Report
        def propagate(assumptions: Assumptions) -> Report

    class Solver:
        def solve(encoding_data: EncodingData, measure: Measure, supplements: Supplements) -> Report
        def propagate(encoding_data: EncodingData, measure: Measure, supplements: Supplements) -> Report
        def use_incremental(encoding_data: EncodingData, measure: Measure, constraints: Constraints) -> IncrSolver:

| The **solve** and **propagate** method is used to solve (or propagate) a task defined in **encoding_data**, taking into account additional **supplements**. Returns an instance of the **Report** class filled with computed data.
| The **use_incremental** method returns instance of incremental solver **IncrSolver** with fixed arguments **encoding_data**, **measure** and **constraints**. The **solve** and **propagate** methods of returned **IncrSolver** instance are accepted arguments only a list of **assumptions**.

The instance of **Report** class is a *NamedTuple* instance, which is set as follows:

.. code-block:: python

    report = Report(
        time: float
        value: float
        status: Status
        model: Optional[Any]
    )

PySAT solvers
-------------

| This implementation wraps solvers from `python-sat <https://pysathq.github.io/docs/html/api/solvers.html#list-of-classes>`_ library.

.. code-block:: python

    from function.module.solver import pysat

    solver = pysat.Glucose3()

2SAT Check
----------

| This implementation is used to check if a task belongs to the 2SAT class.

.. code-block:: python

    from function.module.solver import TwoSAT

    solver = TwoSAT(
        threshold: Optional[float]
    )

Other function modules
----------------------

* `Measure <measure.module.html>`_
