import unittest

import mongoext.scheme as scheme


class TestUnicodeField(unittest.TestCase):
    def setUp(self):
        self.field = scheme.Unicode()

    def test_int(self):
        self.assertEqual(self.field.cast(1), u'1')

    def test_zero(self):
        self.assertEqual(self.field.cast(0), u'0')

    def test_true(self):
        self.assertEqual(self.field.cast(True), u'True')
