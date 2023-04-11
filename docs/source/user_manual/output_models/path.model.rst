WorkPath
========

| This structure is used to represent specific paths.

.. code-block:: python

    class WorkPath:
        def to_path(*dirs: [str, ...]) -> WorkPath
        def to_file(filename: str, *dirs: [str, ...]) -> str

| The **to_path** method returns a new **WorkPath** instance, adding **dirs** to the previous path.
| The **to_file** method returns the path to the file **filename** as a string. If **dirs** are given, it will preliminarily call the **to_path** method.

The instance of **WorkPath** class can be created like this:

.. code-block:: python

    from typing.work_path import WorkPath

    path = WorkPath(
        *dirs: [str, ...],
        root: Optional[str]
    )

By default, **root** is equals to the current (**./**) runtime directory.