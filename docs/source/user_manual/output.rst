Output
======

Logger and parser package.

VectorLog
---------

| Параметры:

* **out_path** -- Utility class for path specifying.
* **log_format** -- Формат в котором пишутся логи. По умолчанию: json line.

.. code-block:: python

    from output.impl import VectorLogs
    from typings.work_path import WorkPath

    logger = VectorLog(
        out_path: WorkPath,
        log_format: LogFormat = LogFormat.JSON_LINE
    )