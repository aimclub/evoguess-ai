Encoding
========

| This module defines the encoding of the problem ....

.. code-block:: python

    class Encoding:
        def get_data() -> EncodingData

    class EncodingData:
        def source() -> string

| The **get_data** method возвращает экземпляр класса, который расширяет абстрактный класс **EncodingData**.
| The **source** method возвращает кодировку в соответствующем формате для записи в файл.

CNF
---

| Реализация для кодировок в конъюнктивной нормальной форме (КНФ).
| Кодировку можно считать из файла **или** задать с помощью списка **from_clauses**.

* **from_file** -- Путь до файла, который содержит кодировку в DIMACS формате.
* **from_clauses** -- A list of the `Clauses <../instance_models/var.model.html#clauses>`_.

.. code-block:: python

    from instance.module.encoding import CNF

    encoding = CNF(
        from_file: Optional[str],
        from_clauses: Optional[Clauses]
    )

| The **get_data** method возвращает экземпляр класса **CNFData**, который расширяет абстрактный класс **EncodingData**.

.. code-block:: python

    class CNFData:
        def max_literal() -> int
        def source(supplements: Supplements) -> string
        def clauses(constraints: Constraints) -> Clauses

| The **max_literal** method возвращает целочисленный номер максимального литерала в формуле.
| The **source** method возвращает кодировку в DIMACS формате с подставленными в неё `Supplements <../instance_models/var.model.html#supplements>`_.
| The **clauses** method возвращает список `Clauses <../instance_models/var.model.html#clauses>`_ с подставленными в неё `Constraints <../instance_models/var.model.html#constraints>`_.

CNF+
----

| Реализация для кодировок CNF+, that extends CNF to include cardinality constraints.
| Кодировку можно считать из файла **или** задать с помощью списка **from_clauses** и **from_atmosts**.

* **from_file** -- Путь до файла, который содержит кодировку в DIMACS формате.
* **from_clauses** -- Список `Clauses <../instance_models/var.model.html#clauses>`_.
* **from_clauses** -- Список `Atmosts <../instance_models/var.model.html#atmosts>`_.

.. code-block:: python

    from instance.module.encoding import CNFP

    encoding = CNFP(
        from_file: Optional[str],
        from_clauses: Optional[Clauses]
        from_atmosts: Optional[Atmosts]
    )

| The **get_data** method возвращает экземпляр класса **CNFPData**, который расширяет класс **CNFData**.

.. code-block:: python

    class CNFPData:
        def max_literal() -> int
        def source(supplements: Supplements) -> string
        def clauses(constraints: Constraints) -> Clauses
        def atmosts() -> Atmosts

| The **max_literal**, **source** and **clauses** method работает аналогичным с **CNFData** образом.
| The **atmosts** method возвращает список `Atmosts <../instance_models/var.model.html#atmosts>`_.

Other instance modules
----------------------

* `Variables <variables.module.html>`_
