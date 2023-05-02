import unittest

# from instance.module.encoding import CNF
# from instance.module.variables import Indexes
# from instance.impl import Instance, StreamCipher
# from core.module.space import SearchSet, InputSet, RhoSubset


class TestSpace(unittest.TestCase):
    pass
    # todo: move to space package test
    # def test_search_set(self):
    #     interval = Indexes(from_iterable=[1, 2, 3, 4])
    #     instance = Instance(encoding=CNF(from_clauses=[]))
    #
    #     space = SearchSet(interval)
    #     self.assertEqual(str(space.get_initial(instance)), '1 2 3 4')
    #
    #     space = SearchSet(interval, by_mask=[])
    #     self.assertEqual(str(space.get_initial(instance)), '')
    #
    #     space = SearchSet(interval, by_mask=[1, 1])
    #     self.assertEqual(str(space.get_initial(instance)), '1 2')
    #
    #     space = SearchSet(interval, by_string='2 3')
    #     self.assertEqual(str(space.get_initial(instance)), '2 3')
    #
    #     space = SearchSet(interval, by_string='2 3 5')
    #     self.assertEqual(str(space.get_initial(instance)), '2 3')
    #
    # def test_input_set(self):
    #     space = InputSet()
    #     instance = StreamCipher(
    #         encoding=CNF(from_clauses=[]),
    #         input_set=Indexes(from_iterable=[1, 2, 3, 4]),
    #         output_set=Indexes(from_iterable=[5, 6, 7, 8])
    #     )
    #     self.assertEqual(str(space.get_initial(instance)), '1 2 3 4')
    #
    #     instance = StreamCipher(
    #         encoding=CNF(from_clauses=[]),
    #         input_set=Indexes(from_iterable=[10, 11, 12]),
    #         output_set=Indexes(from_iterable=[5, 6, 7, 8])
    #     )
    #     self.assertEqual(str(space.get_initial(instance)), '10 11 12')
    #
    # def test_rho_subset(self):
    #     clauses = [[1, 3], [2, -4], [-3, 5], [-4, -6]]
    #     interval = Indexes(from_iterable=[1, 2, 3, 4, 5, 6])
    #     instance = Instance(encoding=CNF(from_clauses=clauses))
    #
    #     space = RhoSubset(variables=interval, of_size=3)
    #     self.assertEqual(str(space.get_initial(instance)), '3 4 5')
    #
    #     space = RhoSubset(variables=interval, of_size=5)
    #     self.assertEqual(str(space.get_initial(instance)), '1 3 4 5 6')
