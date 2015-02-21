import unittest

from . import fixture


class CollectionTestCase(fixture.MongoextTestCase):
    def test_collection_find(self):
        cursor = fixture.Collection().find({'created_ts': {'$gte': 1}}, {'title': 1}, 1).sort('created_ts')
        self.assertTrue(all([lambda: isinstance(c, dict) for c in cursor]))


class EmptyCollectionTestCase(unittest.TestCase):
    def test_collection_count(self):
        pass
