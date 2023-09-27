import unittest
from copy import copy

from pysat import formula as fml

from util.work_path import WorkPath
from pysatmc.encoding import CNF, WCNF


class TestEncodings(unittest.TestCase):
    def test_cnf_from_clause(self):
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        formula = CNF(from_clauses=clauses).get_formula()

        self.assertIsInstance(formula, fml.CNF)
        self.assertEqual(formula.clauses, clauses)
        self.assertEqual(formula.nv, max(map(
            max, [map(abs, c) for c in clauses]
        )))

        constraints = [[-5, 2, -3]]
        formula.extend(constraints)
        self.assertEqual(formula.clauses, clauses + constraints)
        self.assertEqual(formula.nv, max(map(
            max, [map(abs, c) for c in clauses + constraints]
        )))

    def test_cnf_from_file(self):
        root_path = WorkPath('examples', 'data')
        cnf = CNF(from_file=root_path.to_file('a5_1.cnf'))

        formula = cnf.get_formula()
        self.assertEqual(formula.nv, 8425)
        self.assertEqual(formula.clauses[0], [65, 9, 30])
        self.assertEqual(formula.clauses[16], [-68, 17, 65])
        self.assertEqual(formula.clauses[1228], [-335, 268, 333])
        self.assertEqual(formula.clauses[-1], [-8425, -8293, -8295, 8297])

    def test_cnf_copy(self):
        root_path = WorkPath('examples', 'data')
        cnf = CNF(from_file=root_path.to_file('a5_1.cnf'))
        formula, cnf_copy = cnf.get_formula(), copy(cnf)
        copy_formula = cnf_copy.get_formula()

        clauses, copy_clauses = formula.clauses, copy_formula.clauses
        self.assertListEqual(formula.clauses, copy_formula.clauses)
        self.assertEqual(len(clauses), len(copy_clauses))
        self.assertEqual(formula.nv, copy_formula.nv)

    def test_cnf_copy_formula(self):
        root_path = WorkPath('examples', 'data')
        cnf = CNF(from_file=root_path.to_file('a5_1.cnf'))

        self.assertNotEqual(
            cnf.get_formula(), cnf.get_formula()
        )
        self.assertEqual(
            cnf.get_formula(copy=False), cnf.get_formula(copy=False)
        )

    def test_wcnf_from_clause(self):
        # todo: add test_wcnf_from_clause tests
        pass

    def test_wcnf_from_file(self):
        # todo: add test_wcnf_from_file tests
        pass
