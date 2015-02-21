from . import fixture


class CollectionTestCase(fixture.MongoextTestCase):
    def test_collection_find(self):
        cursor = fixture.Collection().find({'about': {'$gte': 1}}, {'about': 1}, 1).sort('about')
        self.assertTrue(all([lambda: isinstance(c, dict) for c in cursor]))
