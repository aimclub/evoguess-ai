import unittest
from copy import copy

from space.model import Backdoor
from typings.searchable import combine

from instance.module.variables import Range, Indexes, Variables
from instance.module.variables.vars import Index, Domain, XorSwitch, get_var_deps


class TestBackdoor(unittest.TestCase):
    def test_backdoor(self):
        backdoor = Backdoor(Range(start=1, length=64))
        self.assertEqual(backdoor.power(), 2 ** 64)
        self.assertEqual(len(backdoor), 64)
        self.assertIn(43, backdoor)

        backdoor_copy = copy(backdoor)
        self.assertEqual(backdoor.get_vector(), [1] * 64)
        self.assertEqual(backdoor.get_vector(), backdoor_copy.get_vector())
        self.assertEqual(backdoor.dependents(), backdoor_copy.dependents())

        backdoor_vector = backdoor.get_vector()[:40] + [0] * 40
        backdoor_40 = backdoor.make_copy(backdoor_vector)

        self.assertNotIn(43, backdoor_40)
        self.assertEqual(backdoor_40.power(), 2 ** 40)
        self.assertEqual(backdoor_40.get_vector(), [1] * 40 + [0] * 24)

        self.assertEqual(backdoor.get_vector(), Backdoor.unpack(backdoor.pack()))

    def test_index_backdoor(self):
        str_iterable = '1 5 9 12 17 21 23 24 25 35'
        backdoor = Backdoor(Indexes(from_string=str_iterable))
        self.assertEqual(len(backdoor), 10)
        self.assertEqual(str(backdoor), str_iterable)
        self.assertEqual(repr(backdoor), f'[{str_iterable}](10)')

        self.assertEqual(backdoor._length, 10)
        self.assertEqual(backdoor._vector, [1] * 10)

        str_vars = str_iterable.split(' ')
        for i, variable in enumerate(backdoor):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str_vars[i])

        int_vars = set(map(int, str_vars))
        self.assertEqual(get_var_deps(backdoor.dependents()), int_vars)
        self.assertEqual(backdoor.dimension(), [2] * len(int_vars))

    def test_vars_backdoor(self):
        backdoor = Backdoor(Variables(from_vars=[
            Domain('d1', [1, 2, 3, 4, 5, 6]),
            Index(7), Index(8), Index(9), Index(10),
            XorSwitch('x1', [11, 12]), XorSwitch('x2', [13, 14])
        ]))
        variables = backdoor.dependents()
        for variable in variables:
            self.assertIn(variable, backdoor)

        self.assertEqual(backdoor, copy(backdoor))
        self.assertNotEqual(backdoor, backdoor.make_copy([1, 1, 1]))

        var_deps = {variables[0], *range(7, 15)}
        self.assertEqual(get_var_deps(backdoor.dependents()), var_deps)

        values = [4, 1, 1, 0, 0, 1, 0]
        alters = ['d1', 7, 8, 9, 10, 'x1', 'x2']
        for var, alt in zip(variables, alters):
            self.assertEqual(var, alt)
        self.assertEqual(str(backdoor), 'd1 7 8 9 10 x1 x2')

        value_dict = {var: value for var, value in zip(backdoor, values)}
        self.assertEqual(value_dict[7], 1)
        self.assertEqual(value_dict['d1'], 4)
        assumptions, constraints = combine(*(
            var.supplements(value_dict) for var in backdoor
        ))
        self.assertEqual(assumptions, [-1, -2, -3, -4, 5, -6, 7, 8, -9, -10])
        self.assertEqual(constraints, [[11, 12], [-11, -12], [13, -14], [-13, 14]])
