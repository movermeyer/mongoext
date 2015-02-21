import unittest

from . import fixture


class FindDocumentTestCase(fixture.MongoextTestCase):
    def setUp(self):
        self.documents = [{
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        }, {
            'title': u'Title2',
            'description': u'Description2',
            'content': u'Content2',
            'created_ts': 2,
        }, {
            'title': u'Title3',
            'description': u'Description3',
            'content': u'Content3',
            'created_ts': 3,
        }]

        fixture.Collection().insert(self.documents)

    def test_find_documents(self):
        documents = [d for d in fixture.Collection().find()]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, self.documents)

    def test_find_documents_by_spec(self):
        spec = {
            'created_ts': 2
        }
        documents = [d for d in fixture.Collection().find(spec)]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, [self.documents[1]])

    def test_find_documents_by_spec_with_empty_result(self):
        spec = {
            'created_ts': -1
        }
        documents = [d for d in fixture.Collection().find(spec)]
        self.assertEqual(documents, [])

    def test_find_documents_by_spec_with_more_the_one_result(self):
        spec = {
            'created_ts': {'$gt': 1},
        }
        documents = [d for d in fixture.Collection().find(spec)]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, self.documents[1:])

    def test_find_documents_with_specified_fields(self):
        documents = [d for d in fixture.Collection().find(fields={'created_ts': 1})]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, [{'created_ts': d['created_ts']} for d in self.documents])
        # cursor = fixture.Collection().find({'created_ts': {'$gte': 1}}, {'title': 1}, 1).sort('created_ts')
        # self.assertTrue(all([lambda: isinstance(c, dict) for c in cursor]))


class EmptyCollectionTestCase(unittest.TestCase):
    def test_collection_count(self):
        pass
