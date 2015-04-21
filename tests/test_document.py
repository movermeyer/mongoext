import unittest

import mongoext.scheme as scheme
import mongoext.collection as collection
import mongoext.document as document


class Collection(collection.Collection):
    CONNECTION = {'host': 'localhost', 'port': 27017}
    DATABASE = 'db'
    NAME = 'collection'


class Document(document.Document):
    client_id = scheme.Numeric()
    content = scheme.Unicode()

    objects = Collection()


class MongoextTestCase(unittest.TestCase):
    def test_init(self):
        document = Document(
            client_id='1',
            content=1,
        )
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
