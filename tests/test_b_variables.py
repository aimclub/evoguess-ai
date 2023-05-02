import unittest

from instance.module.variables import Range, Indexes
from instance.module.variables.vars import Index, Domain, \
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

        interval = Range(from_string=str(_range))
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
