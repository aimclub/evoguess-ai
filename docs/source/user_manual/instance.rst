Instance
========

This package defines models to represent the researched problem under study.

Instance
--------

| An implementation to represent a problem model only through encoding of this problem. It is used if knowledge about the internal structure of the variables is not known or is not required to solve the problem. This implementation is defined by the following parameters:

* **encoding** -- Instance of `Encoding <instance_modules/encoding.module.html>`_ module.

.. code-block:: python

    from instance.impl import Instance

    instance = Instance(
        encoding: Encoding
    )

Stream Cipher
-------------

| An implementation to represent a problem model for which the input and output variable sets are known. Used to work with representations of inversion problems for various functions. You can also specify an additional set of variables to weaken the encoding. The values of weakening variables will also be substituted in the process of constructing the inversion problem.
| This implementation is defined by the following parameters:

* **encoding** -- Instance of `Encoding <instance_modules/encoding.module.html>`_ module.
* **input_set** -- Instance of `Variables <instance_modules/variables.module.html>`_ module.
* **output_set** -- Instance of Indexes in `Variables <instance_modules/variables.module.html>`_ module.
* **extra_set** -- Optional instance of `Variables <instance_modules/variables.module.html>`_ module.

.. code-block:: python

    from instance.impl import StreamCipher

    instance = StreamCipher(
        encoding: Encoding,
        input_set: Indexes,
        output_set: Variables,
        extra_set: Optional[Variables]
    )

Instance modules
----------------

.. toctree::
    :maxdepth: 1

    instance_modules/encoding.module
    instance_modules/variables.module