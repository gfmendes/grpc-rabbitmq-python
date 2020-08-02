import unittest
from client_processor import math_operation


class MathOperationTest(unittest.TestCase):

    def test_when_operand_sum_then_sum_operands(self):
        func = {'operator': 'sum', 'operands': [10, 5, 4]}
        math_operation.MathOperation().calc(func)
        self.assertEqual('success', func['status'])
        self.assertEqual(19, func['result'])
        self.assertIsNotNone(func['uid'])

    def test_when_operand_sub_then_subtract_operands(self):
        func = {'operator': 'sub', 'operands': [10, 5, 4]}
        math_operation.MathOperation().calc(func)
        self.assertEqual('success', func['status'])
        self.assertEqual(1, func['result'])
        self.assertIsNotNone(func['uid'])

    def test_when_operand_mul_then_multiply_operands(self):
        func = {'operator': 'mul', 'operands': [10, 5, 4]}
        math_operation.MathOperation().calc(func)
        self.assertEqual('success', func['status'])
        self.assertEqual(200, func['result'])
        self.assertIsNotNone(func['uid'])

    def test_when_operand_div_then_divide_operands(self):
        func = {'operator': 'div', 'operands': [10, 5, 4]}
        math_operation.MathOperation().calc(func)
        self.assertEqual('success', func['status'])
        self.assertEqual(0.5, func['result'])
        self.assertIsNotNone(func['uid'])

    def test_when_invalid_operator_then_fail_operation(self):
        func = {'operator': 'rrr', 'operands': [10, 5, 4]}
        math_operation.MathOperation().calc(func)
        self.assertEqual('fail', func['status'])
        self.assertIn("Operator 'rrr' not supported", func['result'])
        self.assertIsNotNone(func['uid'])

    def test_when_invalid_operands_then_fail_operation(self):
        func = {'operator': 'sum', 'operands': [10, 5, 'a']}
        math_operation.MathOperation().calc(func)
        self.assertEqual('fail', func['status'])
        self.assertIn("Operands [10, 5, 'a'] not supported", func['result'])
        self.assertIsNotNone(func['uid'])

    def test_when_division_by_zero_then_fail_operation(self):
        func = {'operator': 'div', 'operands': [10, 5, 0]}
        math_operation.MathOperation().calc(func)
        self.assertEqual('fail', func['status'])
        self.assertIn("division by zero", func['result'])
        self.assertIsNotNone(func['uid'])
