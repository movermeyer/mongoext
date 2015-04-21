# import unittest

# import mongoext.fields as fields


# class TestNumericField(unittest.TestCase):
#     def setUp(self):
#         self.field = fields.Numeric()

#     def test_str_number(self):
#         self.assertEqual(self.field('1'), 1)

#     def test_unsupported_str(self):
#         with self.assertRaises(ValueError):
#             self.field('a')


# class TestNumericListField(unittest.TestCase):
#     def setUp(self):
#         self.field = fields.List(fields.Numeric())

#     def test_list_of_valid_strings(self):
#         self.assertEqual(self.field(['1', '2']), [1, 2])

#     def test_empty_list(self):
#         self.assertEqual(self.field([]), [])

#     def test_list_of_invalid_strings(self):
#         with self.assertRaises(ValueError):
#             self.assertEqual(self.field(['a', '2']), ['a', 2])

#     def test_non_iterable_none(self):
#         with self.assertRaises(ValueError):
#             self.field(None)

#     def test_non_iterable_int(self):
#         with self.assertRaises(ValueError):
#             self.field(1)


# class TestStringListField(unittest.TestCase):
#     def setUp(self):
#         self.fields = fields.List(fields.String())


# class TestList(unittest.TestCase):
#     def setUp(self):
#         self.field = fields.List()

#     def test_random_values(self):
#         self.assertEqual(self.field([1, '1']), [1, '1'])

#     def test_empty_list(self):
#         self.assertEqual(self.field([]), [])

#     def test_non_iterable_none(self):
#         with self.assertRaises(ValueError):
#             self.field(None)

#     def test_non_iterable_int(self):
#         with self.assertRaises(ValueError):
#             self.field(1)


# class TestDict(unittest.TestCase):
#     def setUp(self):
#         self.field = fields.Dict()

#     def test_random_values(self):
#         self.assertEqual(self.field({'a': 1}), {'a': 1})

#     def test_empty_dict(self):
#         self.assertEqual(self.field({}), {})

#     def test_non_mapping_none(self):
#         with self.assertRaises(ValueError):
#             self.field(None)

#     def test_non_mapping_int(self):
#         with self.assertRaises(ValueError):
#             self.field(1)


# class TestNumericDict(unittest.TestCase):
#     def setUp(self):
#         self.field = fields.Dict(fields.Numeric())

#     def test_random_values(self):
#         self.assertEqual(self.field({'a': 1}), {'a': 1})

#     def test_random_valid_values(self):
#         self.assertEqual(self.field({'a': '1'}), {'a': 1})

#     def test_empty_dict(self):
#         self.assertEqual(self.field({}), {})

#     def test_invalid_values(self):
#         with self.assertRaises(ValueError):
#             self.field({'a': 'a'})

#     def test_non_mapping_none(self):
#         with self.assertRaises(ValueError):
#             self.field(None)

#     def test_non_mapping_int(self):
#         with self.assertRaises(ValueError):
#             self.field(1)
