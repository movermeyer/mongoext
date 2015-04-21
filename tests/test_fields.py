import unittest

import mongoext.fields as fields


class TestNumericField(unittest.TestCase):
    def setUp(self):
        self.field = fields.Numeric()

    def test_str_number(self):
        self.assertEqual(self.field('1'), 1)

    def test_unsupported_str(self):
        with self.assertRaises(ValueError):
            self.field('a')


class TestNumericListField(unittest.TestCase):
    def setUp(self):
        self.field = fields.List(fields.Numeric())

    def test_list_of_strings(self):
        self.assertEqual(self.field(['1', '2']), [1, 2])
