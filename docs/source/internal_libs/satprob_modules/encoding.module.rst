Encoding Module
===============

| This module for defining the encoding of some `Problem <../lib_satprob.html#problem>`_. In essence, this module is a wrapper over the `formula <https://pysathq.github.io/docs/html/api/formula.html>`_ module of the `pysat <https://pysathq.github.io>`_ library, providing the lazy initialization feature. It also provides a feature to cache initialized object for the executing process.

Encoding
--------

| Module interface for determining the `Problem <../lib_satprob.html#problem>`_ encoding. It has one inherited method: `get_formula(...) <#get_formula>`_, which should return an instance of the corresponding formula.

.. code-block:: python

    class lib_satprob.encoding.Encoding()

| Base **Encoding** class constructor haven't any arguments.

.. function:: get_formula(copy)

    | This method returns instance of encoding formula.

    | Input arguments:

    * ``copy`` (Optional[bool]) - a flag to return a copy of `pysat formula <https://pysathq.github.io/docs/html/api/formula.html>`_ instance instead of original lazily created instance.

    | Return type: Any (defined in a specific implementation).

Clause
^^^^^^

| An alias for the clause type.

.. code-block:: python

    type lib_satprob.encoding.Clause = List[int]

CNF
---

| Module implementation for encodings in conjunctive normal form (CNF). This class is a wrapper over the `pysat.formula.CNF <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.CNF>`_ class.

.. code-block:: python

    class lib_satprob.encoding.CNF(from_file=None: str, from_string=None: str, extract_hard=False: bool, from_clauses=None: List[Clause], comment_lead=['c']: List[str])

| Init arguments:

* ``from_file`` (Optional[str]) - a path to the file containing CNF in DIMACS format. This argument involves **lazily** creation by reading from the given file. Default: ``None``.

* ``from_string`` (Optional[str]) - a string with CNF in DIMACS format. Default: ``None``.

* ``extract_hard`` (Optional[bool]) - a flag to extract hard clauses from the WCNF encoding specified in the given file. Only works with the ``from_file`` argument. Default: ``False``.

* ``from_clauses`` (Optional[List[`Clause <#clause>`_]) - a list of clauses to bootstrap the formula with. Default: ``None``.

* ``comment_lead`` (Optional[List[str]) - a list of characters leading comment lines. Default: ``['c']``.

.. important::

    To create a `CNF <#cnf>`_ instance specify only one initialization argument (``from_file`` **or** ``from_string`` **or** ``from_clauses``).

.. function:: get_formula(copy)
    :noindex:

    | Input arguments:

    * ``copy`` (Optional[bool]) - a flag to return a copy of `pysat.formula.CNF <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.CNF>`_ instance instead of original lazily created instance.

    | Return type: `pysat.formula.CNF <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.CNF>`_

CNFPlus
-------

| Module implementation for CNF encodings augmented with native cardinality constraints. This class is a wrapper over the `pysat.formula.CNFPlus <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.CNFPlus>`_ class.

.. code-block:: python

    class lib_satprob.encoding.CNF(from_file=None: str, from_string=None: str, comment_lead=['c']: List[str])

| Init arguments:

* ``from_file`` (Optional[str]) - a path to the file containing CNF+ in DIMACS format. This argument involves **lazily** creation by reading from the given file. Default: ``None``.

* ``from_string`` (Optional[str]) - a string with CNF+ in DIMACS format. Default: ``None``.

* ``comment_lead`` (Optional[List[str]) - a list of characters leading comment lines. Default: ``['c']``.

.. important::

    To create a `CNFPlus <#cnfplus>`_ instance specify only one initialization argument (``from_file`` **or** ``from_string``).

.. function:: get_formula(copy)
    :noindex:

    | Input arguments:

    * ``copy`` (Optional[bool]) - a flag to return a copy of `pysat.formula.CNFPlus <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.CNFPlus>`_ instance instead of original lazily created instance.

    | Return type: `pysat.formula.CNFPlus <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.CNFPlus>`_

WCNF
----

| Module implementation for partial (weighted) CNF encodings. This class is a wrapper over the `pysat.formula.WCNF <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.WCNF>`_ class.

.. code-block:: python

    class lib_satprob.encoding.WCNF(from_file=None: str, from_string=None: str, comment_lead=['c']: List[str])

| Init arguments:

* ``from_file`` (Optional[str]) - a path to the file containing WCNF in WDIMACS format. This argument involves **lazily** creation by reading from the given file. Default: ``None``.

* ``from_string`` (Optional[str]) - a string with WCNF in WDIMACS format. Default: ``None``.

* ``comment_lead`` (Optional[List[str]) - a list of characters leading comment lines. Default: ``['c']``.

.. important::

    To create a `WCNF <#wcnf>`_ instance specify only one initialization argument (``from_file`` **or** ``from_string``).

.. function:: get_formula(copy)
    :noindex:

    | Input arguments:

    * ``copy`` (Optional[bool]) - a flag to return a copy of `pysat.formula.WCNF <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.WCNF>`_ instance instead of original lazily created instance.

    | Return type: `pysat.formula.WCNF <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.WCNF>`_

WCNFPlus
--------

| Module implementation for CNF encodings augmented with native cardinality constraints. This class is a wrapper over the `pysat.formula.WCNFPlus <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.WCNFPlus>`_ class.

.. code-block:: python

    class lib_satprob.encoding.WCNFPlus(from_file=None: str, from_string=None: str, comment_lead=['c']: List[str])

| Init arguments:

* ``from_file`` (Optional[str]) - a path to the file containing WCNFPlus in WDIMACS format. This argument involves **lazily** creation by reading from the given file. Default: ``None``.

* ``from_string`` (Optional[str]) - a string with WCNFPlus in WDIMACS format. Default: ``None``.

* ``comment_lead`` (Optional[List[str]) - a list of characters leading comment lines. Default: ``['c']``.

.. important::

    To create a `WCNFPlus <#wcnfplus>`_ instance specify only one initialization argument (``from_file`` **or** ``from_string``).

.. function:: get_formula(copy)
    :noindex:

    | Input arguments:

    * ``copy`` (Optional[bool]) - a flag to return a copy of `pysat.formula.WCNFPlus <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.WCNFPlus>`_ instance instead of original lazily created instance.

    | Return type: `pysat.formula.WCNFPlus <https://pysathq.github.io/docs/html/api/formula.html#pysat.formula.WCNFPlus>`_
