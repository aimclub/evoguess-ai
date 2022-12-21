import unittest
from copy import copy

from instance.module.variables import Interval, Indexes, Backdoor
from instance.module.variables.vars import Index, Domain, \
    XorSwitch, Bent4Switch, MajoritySwitch, compress


class TestVariables(unittest.TestCase):
    def test_interval(self):
        interval = Interval(start=1, length=64)
        self.assertEqual(len(interval), 64)
        self.assertEqual(str(interval), '1..64')
        self.assertEqual(repr(interval), '[1..64](64)')

        for i, variable in enumerate(interval):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str(i + 1))

        interval = Interval(from_string=str(interval))
        self.assertEqual(str(interval), '1..64')

    def test_indexes(self):
        iterable = range(31, 67)
        indexes = Indexes(from_iterable=iterable)
        self.assertEqual(len(indexes), len(iterable))
        str_iterable = ' '.join(map(str, iterable))
        self.assertEqual(str(indexes), str_iterable)
        self.assertEqual(repr(indexes), f'[{str_iterable}]({len(iterable)})')

        for i, variable in enumerate(indexes):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str(i + 31))

        interval = Indexes(from_string=str(indexes))
        self.assertEqual(str(interval), str_iterable)

    def test_backdoor(self):
        interval = Interval(start=1, length=64)
        backdoor = Backdoor(from_vars=interval.variables())
        self.assertEqual(backdoor.power(), 2 ** 64)
        self.assertEqual(len(backdoor), 64)
        self.assertIn(43, backdoor)

        backdoor_copy = copy(backdoor)
        self.assertEqual(backdoor.get_mask(), [1] * 64)
        self.assertEqual(backdoor.get_mask(), backdoor_copy.get_mask())
        self.assertEqual(backdoor.variables(), backdoor_copy.variables())

        backdoor_mask = backdoor.get_mask()[:40] + [0] * 40
        backdoor_40 = backdoor.get_copy(backdoor_mask)

        self.assertNotIn(43, backdoor_40)
        self.assertEqual(backdoor_40.power(), 2 ** 40)
        self.assertEqual(backdoor_40.get_mask(), [1] * 40 + [0] * 24)

        self.assertEqual(backdoor.get_mask(), Backdoor.unpack(backdoor.pack()))

    def test_index_backdoor(self):
        str_iterable = '1 5 9 12 17 21 23 24 25 35'
        indexes = Indexes(from_string=str_iterable)
        backdoor = Backdoor(from_vars=indexes.variables())
        self.assertEqual(len(backdoor), 10)
        self.assertEqual(str(backdoor), str_iterable)
        self.assertEqual(repr(backdoor), f'[{str_iterable}](10)')

        self.assertEqual(backdoor._length, 10)
        self.assertEqual(backdoor._mask, [1] * 10)

        str_vars = str_iterable.split(' ')
        for i, variable in enumerate(backdoor):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str_vars[i])

        int_vars = set(map(int, str_vars))
        self.assertEqual(backdoor.get_var_deps(), int_vars)
        self.assertEqual(backdoor.get_deps_bases(), [2] * len(int_vars))

    def test_vars(self):
        index = Index(7)
        self.assertEqual(7, index)
        self.assertEqual('7', index)
        self.assertEqual(index, index)
        self.assertEqual(index, Index(7))
        self.assertEqual(
            (index.supplements({index: 0}),
             index.supplements({index: 1})),
            (([-7], []), ([7], []))
        )
        self.assertEqual(index.supplements({7: 0}), ([-7], []))

        domain = Domain('d1', [1, 2, 3, 4, 5, 6])
        self.assertEqual('d1', domain)
        self.assertEqual(domain, domain)
        self.assertEqual(domain, Domain('d1', [1, 2, 3, 4, 5, 6]))
        self.assertEqual(
            domain.supplements({domain: 1}),
            ([-1, 2, -3, -4, -5, -6], [])
        )
        self.assertEqual(
            domain.supplements({domain: 4}),
            ([-1, -2, -3, -4, 5, -6], [])
        )
        self.assertEqual(
            domain.supplements({1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1}),
            ([-1, -2, -3, -4, -5, 6], [])
        )

        with self.assertRaises(KeyError):
            domain.supplements({1: 0, 2: 0}),

        xor_switch = XorSwitch('x1', [8, 9])
        self.assertEqual(xor_switch, 'x1')
        self.assertEqual(xor_switch, xor_switch)
        self.assertEqual(xor_switch, XorSwitch('x1', [8, 9]))
        self.assertEqual(
            xor_switch.supplements({xor_switch: 1}),
            ([], [[8, 9], [-8, -9]])
        )
        self.assertEqual(
            xor_switch.supplements({8: 1, 9: 1}),
            ([], [[8, -9], [-8, 9]])
        )

        maj_switch = MajoritySwitch('m1', [14, 15, 16])
        self.assertEqual('m1', maj_switch)
        self.assertEqual(maj_switch, maj_switch)
        self.assertEqual(
            maj_switch.supplements({maj_switch: 1}),
            ([], [[14, 15, 16], [14, 15, -16], [14, -15, 16], [-14, 15, 16]])
        )
        self.assertEqual(
            maj_switch.supplements({14: 1, 15: 0, 16: 0}),
            ([], [[14, -15, -16], [-14, 15, -16], [-14, -15, 16], [-14, -15, -16]])
        )

        bent4_switch = Bent4Switch('b1', [10, 11, 12, 13])
        self.assertEqual('b1', bent4_switch)
        self.assertEqual(bent4_switch, bent4_switch)
        self.assertEqual(
            bent4_switch.supplements({bent4_switch: 1}),
            ([], [[10, 11, 12, 13], [10, 11, 12, -13], [10, 11, -12, 13], [10, 11, -12, -13],
                  [10, -11, 12, 13], [10, -11, -12, 13], [-10, 11, 12, 13], [-10, 11, 12, -13],
                  [-10, -11, 12, 13], [-10, -11, -12, -13]])
        )
        self.assertEqual(
            bent4_switch.supplements({10: 1, 11: 0, 12: 0, 13: 0}),
            ([], [[10, -11, 12, -13], [10, -11, -12, -13], [-10, 11, -12, 13], [-10, 11, -12, -13],
                  [-10, -11, 12, -13], [-10, -11, -12, 13]])
        )

        with self.assertRaises(KeyError):
            bent4_switch.supplements({10: 1, 11: 0, 12: 0})

    def test_vars_backdoor(self):
        backdoor = Backdoor(from_vars=[
            Domain('d1', [1, 2, 3, 4, 5, 6]),
            Index(7), Index(8), Index(9), Index(10),
            XorSwitch('x1', [11, 12]), XorSwitch('x2', [13, 14])
        ])
        variables = backdoor.variables()
        for variable in variables:
            self.assertIn(variable, backdoor)

        self.assertEqual(backdoor, copy(backdoor))
        self.assertNotEqual(backdoor, backdoor.get_copy([1, 1, 1]))

        var_deps = {variables[0], *range(7, 15)}
        self.assertEqual(backdoor.get_var_deps(), var_deps)

        values = [4, 1, 1, 0, 0, 1, 0]
        alters = ['d1', 7, 8, 9, 10, 'x1', 'x2']
        for var, alt in zip(variables, alters):
            self.assertEqual(var, alt)
        self.assertEqual(str(backdoor), 'd1 7 8 9 10 x1 x2')

        value_dict = {var: value for var, value in zip(backdoor, values)}
        self.assertEqual(value_dict[7], 1)
        self.assertEqual(value_dict['d1'], 4)
        assumptions, constraints = compress(*(
            var.supplements(value_dict) for var in backdoor
        ))
        self.assertEqual(assumptions, [-1, -2, -3, -4, 5, -6, 7, 8, -9, -10])
        self.assertEqual(constraints, [[11, 12], [-11, -12], [13, -14], [-13, 14]])
