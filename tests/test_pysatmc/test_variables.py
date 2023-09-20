import unittest

from pysatmc.variables import Range, Indexes
from pysatmc.variables.vars import Index, Domain, \
    XorSwitch, Bent4Switch, MajoritySwitch


class TestVariables(unittest.TestCase):
    def test_range(self):
        _range = Range(start=1, length=64)
        self.assertEqual(len(_range), 64)
        self.assertEqual(str(_range), '1..64')
        self.assertEqual(repr(_range), '[1..64](64)')

        for i, variable in enumerate(_range):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str(i + 1))

        _range_2 = Range(from_string=str(_range))
        self.assertEqual(str(_range_2), '1..64')

    def test_indexes(self):
        iterable = range(31, 67)
        _indexes = Indexes(from_iterable=iterable)
        self.assertEqual(len(_indexes), len(iterable))
        str_iterable = ' '.join(map(str, iterable))
        self.assertEqual(str(_indexes), str_iterable)
        repr_iterable = f'[{str_iterable}]({len(iterable)})'
        self.assertEqual(repr(_indexes), repr_iterable)

        for i, variable in enumerate(_indexes):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str(i + 31))

        _indexes_2 = Indexes(from_string=str(_indexes))
        self.assertEqual(str(_indexes_2), str_iterable)

    def test_vars(self):
        index = Index(7)
        self.assertEqual(7, index)
        self.assertEqual('7', index)
        self.assertEqual(index, index)
        self.assertEqual(index, Index(7))
        self.assertEqual(
            (index.substitute({index: 0}),
             index.substitute({index: 1})),
            (([-7], []), ([7], []))
        )
        self.assertEqual(index.substitute({7: 0}), ([-7], []))

        domain = Domain('d1', [1, 2, 3, 4, 5, 6])
        self.assertEqual('d1', domain)
        self.assertEqual(domain, domain)
        self.assertEqual(domain, Domain('d1', [1, 2, 3, 4, 5, 6]))
        self.assertEqual(
            domain.substitute({domain: 1}),
            ([-1, 2, -3, -4, -5, -6], [])
        )
        self.assertEqual(
            domain.substitute({domain: 4}),
            ([-1, -2, -3, -4, 5, -6], [])
        )
        self.assertEqual(
            domain.substitute({
                1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1
            }), ([-1, -2, -3, -4, -5, 6], [])
        )

        with self.assertRaises(KeyError):
            domain.substitute({1: 0, 2: 0}),

        xor_switch = XorSwitch('x1', [8, 9])
        self.assertEqual(xor_switch, 'x1')
        self.assertEqual(xor_switch, xor_switch)
        self.assertEqual(xor_switch, XorSwitch('x1', [8, 9]))
        self.assertEqual(
            xor_switch.substitute({xor_switch: 1}), ([], [[8, 9], [-8, -9]])
        )
        self.assertEqual(
            xor_switch.substitute({8: 1, 9: 1}), ([], [[8, -9], [-8, 9]])
        )

        maj_switch = MajoritySwitch('m1', [14, 15, 16])
        self.assertEqual('m1', maj_switch)
        self.assertEqual(maj_switch, maj_switch)
        self.assertEqual(maj_switch.substitute({maj_switch: 1}), ([], [
            [14, 15, 16], [14, 15, -16], [14, -15, 16], [-14, 15, 16]
        ]))
        self.assertEqual(maj_switch.substitute({14: 1, 15: 0, 16: 0}), ([], [
            [14, -15, -16], [-14, 15, -16], [-14, -15, 16], [-14, -15, -16]
        ]))

        bent4_switch = Bent4Switch('b1', [10, 11, 12, 13])
        self.assertEqual('b1', bent4_switch)
        self.assertEqual(bent4_switch, bent4_switch)
        self.assertEqual(
            bent4_switch.substitute({bent4_switch: 1}), ([], [
                [10, 11, 12, 13], [10, 11, 12, -13], [10, 11, -12, 13],
                [10, 11, -12, -13], [10, -11, 12, 13], [10, -11, -12, 13],
                [-10, 11, 12, 13], [-10, 11, 12, -13], [-10, -11, 12, 13],
                [-10, -11, -12, -13]
            ])
        )
        self.assertEqual(
            bent4_switch.substitute({10: 1, 11: 0, 12: 0, 13: 0}), ([], [
                [10, -11, 12, -13], [10, -11, -12, -13], [-10, 11, -12, 13],
                [-10, 11, -12, -13], [-10, -11, 12, -13], [-10, -11, -12, 13]
            ])
        )

        with self.assertRaises(KeyError):
            bent4_switch.substitute({10: 1, 11: 0, 12: 0})
