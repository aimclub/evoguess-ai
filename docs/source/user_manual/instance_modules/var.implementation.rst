Var
===

Интерфейс для определения различных типов переменных и логики для работы с ними.

Index
------

Реализация для создания обычной индексной переменной.

.. code-block:: python

    from instance.module.variables.vars import Index

    var = Index(index: int)

Domain
------

Реализация для создания виртуальной доменной именованной переменной **name**.
Домен определяется размером списка зависимых переменных **group**.

.. code-block:: python

    from instance.module.variables.vars import Domain

    var = Domain(name: str, group: List[int])

Switch
------

Реализация для создания виртуальной переключаемой именованной переменной **name**.
Подставляемые constranints зависят от значений, принимаемой булевой функцией **op** на различных комбинациях входов зависимых булевых переменных **group**.

.. code-block:: python

    from instance.module.variables.vars import Switch

    var = Switch(name: str, group: List[int], fn: Callable)

XorSwitch
---------

Реализация Switch переменной с заранее определенной функций **fn** как xor.

.. code-block:: python

    from instance.module.variables.vars import XorSwitch

    var = Switch(name: str, group: List[int])

MajoritySwitch
--------------

Реализация Switch переменной с заранее определенной функций **fn** как majority.

.. code-block:: python

    from instance.module.variables.vars import MajoritySwitch

    var = MajoritySwitch(name: str, group: List[int])

Bent4Switch
-----------

Реализация Switch переменной с заранее определенной функций **fn** как bent4.

.. code-block:: python

    from instance.module.variables.vars import Bent4Switch

    var = Bent4Switch(name: str, op: Callable, group: List[int])

Examples
--------

Примеры создания **Index**, **Domain** and **Switch** объектных переменных, и их влияние на решаемую кодировку, при подстановке значений.

.. code-block:: python

    from instance.module.variables.vars import Index, Domain, XorSwitch

    index_var = Index(33)
    # if variable 33 equals 1, then add assumptions [33] to cnf
    # if variable 33 equals 0, then add assumptions [-33] to cnf

    switch_var = XorSwitch('s1', [3, 4])
    # if variable s1 equals 0, then add constraints [[3, -4], [-3, 4]] to cnf
    # if variable s1 equals 1, then add constraints [[3, 4], [-3, -4]] to cnf

    domain_var = Domain('d1', [1, 2, 3, 4, 5]) # domain equals 5
    # if variable d1 equals 1, then add assumptions [1, -2, -3, -4, -4] to cnf
    # if variable d1 equals 3, then add assumptions [-1, -2, 3, -4, -4] to cnf

