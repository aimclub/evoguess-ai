Solver
=======

SAT-solver.

PySAT solvers
-------------

Wrapper of pysat solvers

.. code-block:: python

    from function.module.solver.impl.pysat import Glucose3

    solver = Glucose3()

2SAT Check
----------

Solver to check cnf instance is 2SAT or not.

.. code-block:: python

    from function.module.solver import TwoSAT

    solver = TwoSAT()
