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

    def test_list_of_valid_strings(self):
        self.assertEqual(self.field(['1', '2']), [1, 2])

    def test_empty_list(self):
        self.assertEqual(self.field([]), [])

    def test_list_of_invalid_strings(self):
        with self.assertRaises(ValueError):
            self.assertEqual(self.field(['a', '2']), ['a', 2])

    def test_non_iteratable_none(self):
        with self.assertRaises(ValueError):
            self.field(None)

    def test_non_iterable_int(self):
        with self.assertRaises(ValueError):
            self.field(1)


class TestStringListField(unittest.TestCase):
    def setUp(self):
        self.fields = fields.List(fields.String())
