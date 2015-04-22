import unittest

import mongoext.collection as collection
import mongoext.document as document
import mongoext.exc as exc
import mongoext.scheme as scheme


class Collection(collection.Collection):
    CONNECTION = {'host': 'localhost', 'port': 27017}
    DATABASE = 'db'
    NAME = 'collection'


class Document(document.Document):
    client_id = scheme.Numeric(required=True)
    content = scheme.Unicode()

    objects = Collection()


def tearDownModule():
    Collection().drop()


class TestInitialization(unittest.TestCase):
    def test_full_success(self):
        Document(client_id=1, content='content')

    def test_partial_success(self):
        Document(content='content')

    def test_undefined_field(self):
        with self.assertRaises(exc.SchemeError):
            Document(user_id=1)

    def test_empty_initialization(self):
        Document()


class TestSetAttribute(unittest.TestCase):
    def setUp(self):
        self.document = Document()

    def test_set_undefined_attribute(self):
        self.document.user_id = 1

    def test_set_defined_attribute(self):
        self.document.content = 'content'

    def test_set_defined_attribute_cast_failure(self):
        with self.assertRaises(exc.CastError):
            self.document.client_id = 'a'


class TestToDict(unittest.TestCase):
    def test_full_document(self):
        data = {
            'client_id': 1,
            'content': 'content',
        }
        document = Document(**data)
        self.assertEqual(document.to_dict(), dict(data, _id=None))

    def test_partial_document(self):
        document = Document(client_id=1)
        self.assertEqual(document.to_dict(), {
            '_id': None,
            'client_id': 1,
            'content': None,
        })


class TestRepr(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Document()), '<Document: None>')


class TestSave(unittest.TestCase):
    def test_save(self):
        document = Document()
        document.client_id = 1
        document.content = 'content'
        document.save()

    def test_scheme_error_save(self):
        document = Document()
        document.content = 'content'
        with self.assertRaises(exc.SchemeError):
            document.save()

# from . import fixture


# class ModelTestCase(fixture.MongoextTestCase):
#     def test_find(self):
#         fields = {
#             'created_ts': 1,
#             'title': 1,
#         }
#         cursor = fixture.Document.objects.find({'created_ts': {'$gte': 1}}, fields).sort('created_ts')
#         self.assertTrue(all([lambda: isinstance(c, fixture.Document) for c in cursor]))

#     def test_save(self):
#         cursor = fixture.Document.objects.find({'created_ts': {'$gte': 1}}).sort('created_ts')
#         model = [c for c in cursor][0]
#         model.save()

#     def test_fail_save(self):
#         fields = {
#             'created_ts': 1,
#             'title': 1,
#         }
#         cursor = fixture.Document.objects.find({'created_ts': {'$gte': 1}}, fields).sort('created_ts')
#         model = [c for c in cursor][0]
#         model.created_ts = None
#         with self.assertRaises(ValueError):
#             model.save()

#     def test_fail_insert(self):
#         with self.assertRaises(TypeError):
#             fixture.Document.objects.insert_one(True)

#     def test_repr(self):
#         model = fixture.Document.objects.find_one()
#         self.assertTrue(isinstance(repr(model), basestring))
