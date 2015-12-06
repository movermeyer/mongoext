import unittest

import mongoext.collection as collection
import mongoext.document as document
import mongoext.scheme as scheme
import mongoext.exc as exc

from . import (
    fixture,
    utils,
)


class Document(document.Document):
    content = scheme.String()
    client_id = scheme.Integer()


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
        self.assertEqual(dict(document), data)

    def test_partial_document(self):
        document = Document(client_id=1)
        self.assertEqual(dict(document), {
            'client_id': 1,
        })


class TestRepr(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Document()), '<Document: None>')


class Collection(collection.Collection):
    CONNECTION = utils.get_connection()

    DATABASE = 'db'
    NAME = 'collection'


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


class ModelTestCase(fixture.MongoextTestCase):
    def test_find(self):
        fields = {
            'created_ts': 1,
            'title': 1,
        }
        cursor = fixture.Collection(fixture.Document).find({'created_ts': {'$gte': 1}}, fields).sort('created_ts')
        self.assertTrue(all([lambda: isinstance(c, fixture.Document) for c in cursor]))

    def test_save(self):
        cursor = fixture.Collection(fixture.Document).find({'created_ts': {'$gte': 1}}).sort('created_ts')
        model = [c for c in cursor][0]
        fixture.Collection(fixture.Document).save(model)

    def test_fail_save(self):
        fields = {
            'created_ts': 1,
            'title': 1,
        }
        cursor = fixture.Collection(fixture.Document).find({'created_ts': {'$gte': 1}}, fields).sort('created_ts')
        model = [c for c in cursor][0]
        model.created_ts = None
        with self.assertRaises(exc.ValidationError):
            fixture.Collection(fixture.Document).save(model)

    def test_fail_insert(self):
        with self.assertRaises(TypeError):
            fixture.Collection(fixture.Document).insert_one(True)

    def test_repr(self):
        model = fixture.Collection(fixture.Document).find_one()
        self.assertTrue(isinstance(repr(model), str))
