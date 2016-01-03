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
    client_id = scheme.Integer(required=True)


class InheritedDocument(Document):
    author_id = scheme.Integer()


class ChangedDocument(Document):
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
            'content': u'content',
        }
        document = Document(**data)
        self.assertEqual(dict(document), data)

    def test_partial_document(self):
        document = Document(client_id=1)
        self.assertEqual(dict(document), {
            'client_id': 1,
        })

    def test_inherited_document(self):
        document = InheritedDocument(client_id=1, author_id=1)
        expected = {
            'client_id': 1,
            'author_id': 1,
        }
        self.assertEqual(dict(document), expected)

    def test_changed_inherited_document(self):
        document = ChangedDocument(content='')
        self.assertEqual(document.content, '')


class TestRepr(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Document()), '<Document: None>')


class TestDictBehavior(unittest.TestCase):
    def test_getitem(self):
        document = InheritedDocument(client_id=1)
        self.assertEqual(document['client_id'], 1)

    def test_setitem(self):
        document = Document(client_id=1)
        document['author_id'] = 2
        self.assertEqual(document['author_id'], 2)

    def test_delitem(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertIsNotNone(document['author_id'])
        del document['author_id']
        with self.assertRaises(KeyError):
            self.assertIsNone(document['author_id'])

    def test_get(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertIsNotNone(document.get('author_id'))
        self.assertIsNone(document.get('author_ids'))

    def test_iteration(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertEqual(dict(document), {'client_id': 1, 'author_id': 2})

    def test_keys(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertEqual(set(document.keys()), {'client_id', 'author_id'})

    def test_values(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertEqual(set(document.values()), {1, 2})

    def test_items(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertEqual(set(document.items()), {('client_id', 1), ('author_id', 2)})

    def test_pop(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertEqual(document.pop('client_id'), 1)

    def test_pop_default(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertEqual(document.pop('client_ids', 3), 3)

    def test_pop_fail(self):
        document = InheritedDocument(client_id=1, author_id=2)
        with self.assertRaises(KeyError):
            document.pop('client_ids')

    def test_popitem(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertTrue(document.popitem() in {('client_id', 1), ('author_id', 2)})

    def test_popitem_fail(self):
        document = InheritedDocument()
        with self.assertRaises(KeyError):
            document.popitem()

    def test_clear(self):
        document = InheritedDocument(client_id=1, author_id=2)
        document.clear()
        self.assertEqual(document, InheritedDocument())

    def test_setdefault(self):
        document = InheritedDocument(client_id=1)
        document.setdefault('author_id')
        self.assertIsNone(document['author_id'])


class TestObjectBehavior(unittest.TestCase):
    def test_getitem(self):
        document = InheritedDocument(client_id=1)
        self.assertEqual(document.client_id, 1)

    def test_setitem(self):
        document = Document(client_id=1)
        document.author_id = 2
        self.assertEqual(document.author_id, 2)

    def test_delitem(self):
        document = InheritedDocument(client_id=1, author_id=2)
        self.assertIsNotNone(document.author_id)
        del document.author_id
        with self.assertRaises(AttributeError):
            self.assertIsNone(document.author_id)


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
