SatProb Library
===============

| The SatProb library is used to work with SAT (including MaxSAT) problems. Provides a set of tools for working with SAT and MaxSAT encodings of problems (`Encoding module <./satprob_modules/encoding.module.html>`_), allows you to define sets of variables on these problems (`Variables module <./satprob_modules/variables.module.html>`_), and also provides tools for solving them (`Solver module <./satprob_modules/solver.module.html>`_), to substitute weakening assumptions and constraints for each task.

Problem
-------

| Main class for defining a SAT or MaxSAT problem. The constructor of `Problem <lib_satprob.html#problem>`_ has two mandatory arguments ``encoding`` and ``solver``, and two optional arguments ``input_set`` and ``output_sat``.

.. code-block:: python

    class lib_satprob.Problem(
        solver: Solver,
        encoding: Encoding,
        input_set=None: Indexes,
        output_set=None: Variables
    )

| Init arguments:

* ``solver`` (`Solver <satprob_modules/solver.module.html>`_) - a some algorithm that used to solve the original problem, or problems weakened by substitutions.

* ``encoding`` (`Encoding <satprob_modules/encoding.module.html>`_) - a formula that encodes the original problem.

.. note::

    The solver module has only one implementation `SATSolver <satprob_modules/solver.module.html#satsolver>`_, which automatically detects the kind of problem (SAT or MaxSAT).

* ``input_set`` (Optional[`Indexes <satprob_modules/variables.module.html#indexes>`_]) - a set of input variables in a given encoding. Default: `None`.

* ``output_set`` (Optional[`Variables <satprob_modules/variables.module.html>`_]) - a set of output variables in a given encoding. Default: `None`.

.. important::

    The ``input_set`` and ``output_set`` arguments are used to represent function inversion problems, and must always be specified **together**, or not specified at all.

.. function:: solve(decomposition, with_input_values, with_input_var_map, with_output_values, with_output_var_map, with_random_state)

    | This method is used to solve (see below what it makes for different problems) the given problem using the given solver. If argument ``decomposition`` is provided, then given problem will be decomposed into several sub-problems using the given ``decomposition`` variable set.

    | For different problem the method **solve** makes the following:

    * For SAT problem - this method is used to check satisfiability of a given CNF encoding. If encoding is been satisfiable then returns a `Report <satprob_modules/solver.module.html#report>`_ with **status** is ``True`` and the first found solution as **model**, or `Report <satprob_modules/solver.module.html#report>`_ with **status** is ``False`` otherwise.

    * For MaxSAT problem - this method is used to maximize weight of satisfiable clauses of a given WCNF encoding. If hard clauses of encoding is unsatisfiable then returns a `Report <satprob_modules/solver.module.html#report>`_ with **status** is ``False``, or `Report <satprob_modules/solver.module.html#report>`_ with **status** is ``True`` and the found **cost**. For the complete algorithm, the found cost is the maximum if no **limit** is used.

    | Input arguments:

    * ``decomposition`` (Optional[`Enumerable <satprob_modules/variables.module.html>`_]) - a variable set that is used to decompose the original problem into several sub-problems. Default: ``None``.

    * ``with_input_values`` (Optional[List[int]]) - a values of input variables that are used to generate output values. Default: ``None``.

    * ``with_input_var_map`` (Optional[`VarMap <satprob_models/var.model.html#varmap>`_]) - a map of input variables values that is used to generate output values. Default: ``None``.

    * ``with_output_values`` (Optional[List[int]]) - a values of output variables that will be substituted into the original problem. Default: ``None``.

    * ``with_output_var_map`` (Optional[`VarMap <satprob_models/var.model.html#varmap>`_]) - a map of variable values that will be used when substituting the values of output variables into the original problem. Default: ``None``.

    * ``with_random_state`` (Optional[`RandomState <https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState>`_]) - a state that is used in `Enumerable.enumerate(...) <satprob_models/enumerable.models.html#enumerable>`_ method to generate permutation of decomposition substitutions. Default: ``None``.

    | Return type: `Report <satprob_modules/solver.module.html#report>`_.

    | Example: ...

.. function:: process_output_var_map(with_random_state, from_input_values, from_input_var_map)

    | The method ``process_output_var_map`` is used to propagate output `VarMap <satprob_models/var.model.html#varmap>`_ from input values. If arguments ``from_input_values`` and ``from_input_var_map`` are not provided, then `RandomState <https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState>`_ is used to generate random values for the input variables. If argument **with_random_state** is not provided, then a new state is created without a seed.

    | Input arguments:

    * ``with_random_state`` (Optional[`RandomState <https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState>`_]) - a state that is used to generate random values for the input variables. Default: ``None``.

    * ``from_input_values`` (Optional[List[int]]) - a values of input variables that are used to propagate output `VarMap <satprob_models/var.model.html#varmap>`_. Default: ``None``.

    * ``from_input_var_map`` (Optional[`VarMap <satprob_models/var.model.html#varmap>`_]) - a map of input variables values that is used to propagate output `VarMap <satprob_models/var.model.html#varmap>`_. Default: ``None``.

    | Return type: `VarMap <satprob_models/var.model.html#varmap>`_.

    | Example: ...

.. function:: process_output_supplements(with_random_state, from_input_values, from_input_var_map)

    | The method ``process_output_supplements`` is used to propagate output `Supplements <satprob_modules/variables.module.html#supplements>`_ from input values.

    | Input arguments:

    * ``with_random_state`` (Optional[`RandomState <https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState>`_]) - a state that is used to generate random values for the input variables. Default: ``None``.

    * ``from_input_values`` (Optional[List[int]]) - a values of input variables that are used to propagate output `Supplements <satprob_modules/variables.module.html#supplements>`_. Default: ``None``.

    * ``from_input_var_map`` (Optional[`VarMap <satprob_models/var.model.html#varmap>`_]) - a map of input variables values that is used to propagate output `Supplements <satprob_modules/variables.module.html#supplements>`_. Default: ``None``.

    | Return type: `Supplements <satprob_modules/variables.module.html#supplements>`_

    | Example: ...

SATProblem
----------

| This class clarifies problem (only CNF formulas) and used in dependent classes for stronger typing.

.. code-block:: python

    class lib_satprob.SATProblem(
        solver: Solver,
        encoding: CNF,
        input_set: Optional[Indexes],
        output_set: Optional[Variables]
    )

| The ``encoding`` argument defines the formula of SAT problem in CNF format, and expects an instance of the `CNF <satprob_modules/encoding.module.html#cnf>`_ class.

MaxSATProblem
-------------

| This class also clarifies problem (only WCNF formulas) and used in dependent classes for stronger typing.

.. code-block:: python

    class lib_satprob.MaxSATProblem(
        solver: Solver,
        encoding: WCNF,
        input_set: Optional[Indexes],
        output_set: Optional[Variables]
    )

| The ``encoding`` argument defines the formula of MaxSAT problem in WCNF format, and expects an instance of the `WCNF <satprob_modules/encoding.module.html#wcnf>`_ class.

SatProb models
--------------

.. toctree::
    :maxdepth: 1

    satprob_models/var.model
    satprob_models/solver.model

SatProb modules
---------------

.. toctree::
    :maxdepth: 1

    satprob_modules/solver.module
    satprob_modules/encoding.module
    satprob_modules/variables.module
