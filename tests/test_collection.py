import unittest

from . import fixture


class CollectionFindTestCase(fixture.MongoextTestCase):
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
        }]

        fixture.Collection().insert(self.documents)

    def test_find_document(self):
        documents = [d for d in fixture.Collection().find()]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, self.documents)

        # cursor = fixture.Collection().find({'created_ts': {'$gte': 1}}, {'title': 1}, 1).sort('created_ts')
        # self.assertTrue(all([lambda: isinstance(c, dict) for c in cursor]))


class EmptyCollectionTestCase(unittest.TestCase):
    def test_collection_count(self):
        pass
