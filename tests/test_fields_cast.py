import unittest

import mongoext.scheme as scheme
import mongoext.exc as exc


class TestUnicodeField(unittest.TestCase):
    def setUp(self):
        self.field = scheme.Unicode()

    def test_int(self):
        self.assertEqual(self.field.cast(1), u'1')

    def test_zero(self):
        self.assertEqual(self.field.cast(0), u'0')

    def test_true(self):
        self.assertEqual(self.field.cast(True), u'True')


class TestListField(unittest.TestCase):
    def setUp(self):
        self.field = scheme.List()

    def test_list(self):
        self.assertEqual(self.field.cast([0, 1]), [0, 1])

    def test_tuple(self):
        self.assertEqual(self.field.cast((0, 1)), [0, 1])

    def test_dict(self):
        self.assertEqual(self.field.cast({'a': 1}), ['a'])

    def test_int(self):
        with self.assertRaises(exc.CastError):
            self.field.cast(1)


class TestListNumericField(unittest.TestCase):
    def setUp(self):
        self.field = scheme.List(scheme.Numeric())

    def test_list(self):
        self.assertEqual(self.field.cast([0, 1]), [0, 1])

    def test_str(self):
        self.assertEqual(self.field.cast(['0', '1']), [0, 1])

    def test_invalid_str(self):
        with self.assertRaises(exc.CastError):
            self.field.cast(['a'])


class TestInvalidListField(unittest.TestCase):
    def test_int(self):
        with self.assertRaises(exc.SchemeError):
            scheme.List(int)

    def test_class_field(self):
        scheme.List(scheme.Numeric)
        with self.assertRaises(exc.SchemeError):
            scheme.List(scheme.Numeric)
