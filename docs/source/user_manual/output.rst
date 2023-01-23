Output
======

| This package contains tools for logging the results of experiments and for parsing these results for further analysis.

OptimizeLogger
--------------

| This implementation is defined by the following parameters:

* **out_path** -- Instance of `WorkPath <output_models/path.model.html>`_ class with specified path.
* **log_format** -- The format in which the logs will be written. Default: **LogFormat.JSON_LINE**.

.. code-block:: python

    from output.impl import OptimizeLogger
    from typings.work_path import WorkPath

    logger = OptimizeLogger(
        out_path: WorkPath,
        log_format: Optional[LogFormat]
    )

OptimizeParser
--------------

| This implementation is defined by the following parameters:

* **out_path** -- Instance of `WorkPath <output_models/path.model.html>`_ class with specified path.
* **log_format** -- The format in which the logs were written. Default: **LogFormat.JSON_LINE**.

.. code-block:: python

    from output.impl import OptimizeParser
    from typings.work_path import WorkPath

    parser = OptimizeParser(
        out_path: WorkPath,
        log_format: Optional[LogFormat]
    )

Output models
-------------

.. toctree::
    :maxdepth: 1

    output_models/path.model
