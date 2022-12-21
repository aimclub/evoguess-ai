import unittest

from instance.impl import Instance, StreamCipher
from instance.module.encoding import CNF
from instance.module.variables import Indexes


class RandomStateStub:
    def __init__(self, values=()):
        self.values = values

    def randint(self, *args):
        return self.values


class TestInstance(unittest.TestCase):
    def test_instance(self):
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        instance = Instance(encoding=CNF(from_clauses=clauses))

        self.assertEqual(instance.get_instance_vars(), None)

        indexes = Indexes(from_iterable=[4])
        i_vars = instance.get_instance_vars(indexes)
        self.assertListEqual(i_vars.dependent_vars, indexes.variables())

        self.assertEqual(i_vars.get_propagation(RandomStateStub()), ([], []))
        self.assertEqual(i_vars.get_dependent([1, 2, -3, -4]), ([-4], []))
        self.assertEqual(i_vars.get_dependent([1, 2, -3, 4, 5]), ([4], []))

    def test_stream_cipher(self):
        clauses = [[1, 3], [2, -4], [-3, 5], [-4, -6]]
        instance = StreamCipher(
            encoding=CNF(from_clauses=clauses),
            input_set=Indexes(from_iterable=[1, 2]),
            output_set=Indexes(from_iterable=[5, 6])
        )

        i_vars = instance.get_instance_vars()
        self.assertListEqual(i_vars.dependent_vars, instance.output_set.variables())
        self.assertListEqual(i_vars.propagation_vars, instance.input_set.variables())

        self.assertEqual(i_vars.get_propagation(RandomStateStub([1, 1])), ([1, 2], []))
        self.assertEqual(i_vars.get_propagation(RandomStateStub([0, 1])), ([-1, 2], []))
        self.assertEqual(i_vars.get_dependent([1, 2, -3, -5, 6]), ([-5, 6], []))
        self.assertEqual(i_vars.get_dependent([1, 2, 3, -4, 5, 6]), ([5, 6], []))
