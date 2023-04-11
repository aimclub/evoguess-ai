Instance
========

This package defines models to represent the problem under study.

Instance
--------

| An implementation to represent a model of problem only through **encoding** of this problem. It is used if knowledge about the internal structure of the variables is not known or is not required to solve the problem. This implementation is defined by the following parameters:

* **encoding** -- An instance of the `Encoding <instance_modules/encoding.module.html>`_ module.

.. code-block:: python

    from instance.impl import Instance

    instance = Instance(
        encoding: Encoding
    )

Stream Cipher
-------------

| An implementation to represent a model of problem for which the **input_set** and **output_set** of variables are known. Used to work with representations of inversion problems for various functions. You can also specify an **extra_set** of variables to weaken the encoding. The values of weakening variables will also be substituted in the process of constructing the inversion problem.
| This implementation is defined by the following parameters:

* **encoding** -- An instance of the `Encoding <instance_modules/encoding.module.html>`_ module.
* **input_set** -- An instance of the `Variables <instance_modules/variables.module.html>`_ module.
* **output_set** -- An instance of the `Indexes <instance_modules/variables.module.html#indexes>`_ module.
* **extra_set** -- An optional instance of the `Variables <instance_modules/variables.module.html>`_ module.

.. code-block:: python

    from instance.impl import StreamCipher

    instance = StreamCipher(
        encoding: Encoding,
        input_set: Indexes,
        output_set: Variables,
        extra_set: Optional[Variables]
    )

Instance models
---------------

.. toctree::
    :maxdepth: 1

    instance_models/var.model

Instance modules
----------------

.. toctree::
    :maxdepth: 1

    instance_modules/encoding.module
    instance_modules/variables.module