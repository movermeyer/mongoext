import unittest

import mongoext.collection as collection
import mongoext.document as document
import mongoext.schema as schema
import mongoext.exc as exc


class Document(document.Document):
    content = schema.String()
    client_id = schema.Integer() & schema.Required()


class TestInitialization(unittest.TestCase):
    def test_full_success(self):
        Document(client_id=1, content='content')

    def test_partial_success(self):
        Document(content='content')

    def test_undefined_field(self):
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
        with self.assertRaises(exc.ValidationError):
            self.document.client_id = 'a'


class TestToDict(unittest.TestCase):
    def test_full_document(self):
        data = {
            'client_id': 1,
            'content': 'content',
        }
        document = Document(**data)
        self.assertEqual(dict(document), dict(data, _id=None))

    def test_partial_document(self):
        document = Document(client_id=1)
        self.assertEqual(dict(document), {
            '_id': None,
            'client_id': 1,
            'content': None,
        })


class TestRepr(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Document()), '<Document: None>')


class Collection(collection.Collection):
    CONNECTION = {'host': 'localhost', 'port': 27017}

    DATABASE = 'db'
    NAME = 'collection'


def tearDownModule():
    Collection(Document).drop()


class TestSave(unittest.TestCase):
    def setUp(self):
        self.collection = Collection(Document)

    def test_save(self):
        document = Document()
        document.client_id = 1
        document.content = 'content'
        self.collection.save(document)
        self.assertIsNotNone(document._id)

    def test_update(self):
        document = Document()
        document.client_id = 1
        document.content = 'content'
        self.collection.save(document)
        document.content = u''
        self.collection.save(document)
        document = self.collection.find_one(document._id)
        self.assertEqual(document.content, u'')

    def test_scheme_error_save(self):
        document = Document()
        document.content = 'content'
        with self.assertRaises(exc.ValidationError):
            self.collection.save(document)

