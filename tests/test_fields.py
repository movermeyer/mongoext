# import datetime
# import unittest

# import mongoext.scheme as scheme
# import mongoext.exc as exc


# class TestNumeric(unittest.TestCase):
#     def setUp(self):
#         self.field = scheme.Numeric()

#     def test_str_number(self):
#         self.assertEqual(self.field.cast('1'), 1)

#     def test_unsupported_str(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast('a')


# class TestUnicodeField(unittest.TestCase):
#     def setUp(self):
#         self.field = scheme.Unicode()

#     def test_int(self):
#         self.assertEqual(self.field.cast(1), u'1')

#     def test_zero(self):
#         self.assertEqual(self.field.cast(0), u'0')

#     def test_true(self):
#         self.assertEqual(self.field.cast(True), u'True')


# class TestList(unittest.TestCase):
#     def setUp(self):
#         self.field = scheme.List()

#     def test_random_values(self):
#         self.assertEqual(self.field.cast([1, '1']), [1, '1'])

#     def test_empty_list(self):
#         self.assertEqual(self.field.cast([]), [])

#     def test_non_iterable_none(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast(None)

#     def test_non_iterable_int(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast(1)


# class TestNumericListField(unittest.TestCase):
#     def setUp(self):
#         self.field = scheme.List(scheme.Numeric())

#     def test_list_of_valid_strings(self):
#         self.assertEqual(self.field.cast(['1', '2']), [1, 2])

#     def test_empty_list(self):
#         self.assertEqual(self.field.cast([]), [])

#     def test_list_of_invalid_strings(self):
#         with self.assertRaises(exc.CastError):
#             self.assertEqual(self.field.cast(['a', '2']), ['a', 2])

#     def test_non_iterable_none(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast(None)

#     def test_non_iterable_int(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast(1)


# class TestInvalidListField(unittest.TestCase):
#     def test_int(self):
#         with self.assertRaises(exc.SchemeError):
#             scheme.List(int)

#     def test_class_field(self):
#         with self.assertRaises(exc.SchemeError):
#             scheme.List(scheme.Numeric)


# class TestDateTimeAutoadd(unittest.TestCase):
#     def setUp(self):
#         self.field = scheme.DateTime(autoadd=True)

#     def test_auto_add(self):
#         dt = self.field.cast(None)
#         self.assertTrue(isinstance(dt, datetime.datetime))


# class TestDateTime(unittest.TestCase):
#     def setUp(self):
#         self.field = scheme.DateTime()

#     def test_auto_add(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast(None)


# class TestDict(unittest.TestCase):
#     def setUp(self):
#         self.field = scheme.Dict()

#     def test_random_values(self):
#         self.assertEqual(self.field.cast({'a': 1}), {'a': 1})

#     def test_empty_dict(self):
#         self.assertEqual(self.field.cast({}), {})

#     def test_non_mapping_none(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast(None)

#     def test_non_mapping_int(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast(1)


# class TestNumericDict(unittest.TestCase):
#     def setUp(self):
#         self.field = scheme.Dict(scheme.Numeric())

#     def test_random_values(self):
#         self.assertEqual(self.field.cast({'a': 1}), {'a': 1})

#     def test_random_valid_values(self):
#         self.assertEqual(self.field.cast({'a': '1'}), {'a': 1})

#     def test_empty_dict(self):
#         self.assertEqual(self.field.cast({}), {})

#     def test_invalid_values(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast({'a': 'a'})

#     def test_non_mapping_none(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast(None)

#     def test_non_mapping_int(self):
#         with self.assertRaises(exc.CastError):
#             self.field.cast(1)
