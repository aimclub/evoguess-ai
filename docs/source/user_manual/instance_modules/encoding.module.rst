Encoding
========

| This module defines the encoding of the problem under study.

.. code-block:: python

    class Encoding:
        def get_data() -> EncodingData

    class EncodingData:
        def source() -> string

| The **get_data** method returns a new class instance that extends the **EncodingData** abstract class.
| The **source** method returns a encoding in the format to be written to the file.

CNF
---

| Implementation for encodings in conjunctive normal form (CNF).
| The encoding can be read from a file **or** specified using the **Clauses** list.

.. code-block:: python

    Clauses = List[List[int]]

* **from_file** -- A Path to the file containing the encoding in DIMACS format.
* **from_clauses** -- A list of **Clauses**.

.. code-block:: python

    from instance.module.encoding import CNF

    encoding = CNF(
        from_file: Optional[str],
        from_clauses: Optional[Clauses]
    )

| The **get_data** method returns a new **CNFData** instance that extends the **EncodingData** abstract class.

.. code-block:: python

    class CNFData:
        def max_literal() -> int
        def source(supplements: Supplements) -> string
        def clauses(constraints: Constraints) -> Clauses

| The **max_literal** method returns the number of the maximum literal in the formula.
| The **source** method returns the encoding in DIMACS format with `Supplements <../instance_models/var.model.html>`_ substituted into it.
| The **clauses** method returns a list of **Clauses** with `Constraints <../instance_models/var.model.html>`_ substituted into it.

CNF+
----

| Implementation for CNF+ encodings, that extends CNF to include cardinality constraints.
| The encoding can be read from a file **or** specified using the **Clauses** and **Atmosts** lists.

.. code-block:: python

    Atmosts = List[Tuple[List[int], int]]

* **from_file** -- A Path to the file containing the encoding in DIMACS format.
* **from_clauses** -- A list of **Clauses**.
* **from_clauses** -- A list of **Atmosts**.

.. code-block:: python

    from instance.module.encoding import CNFP

    encoding = CNFP(
        from_file: Optional[str],
        from_clauses: Optional[Clauses]
        from_atmosts: Optional[Atmosts]
    )

| The **get_data** method returns a new **CNFPData** instance that extends the **CNFData** class.

.. code-block:: python

    class CNFPData:
        def max_literal() -> int
        def source(supplements: Supplements) -> string
        def clauses(constraints: Constraints) -> Clauses
        def atmosts() -> Atmosts

| The **max_literal** method returns the number of the maximum literal in the formula.
| The **source** method returns the encoding in DIMACS format with `Supplements <../instance_models/var.model.html>`_ substituted into it.
| The **clauses** method returns a list of **Clauses** with `Constraints <../instance_models/var.model.html>`_ substituted into it.
| The **atmosts** method returns a list of **Atmosts** in the given encoding.

Other instance modules
----------------------

* `Variables <variables.module.html>`_
