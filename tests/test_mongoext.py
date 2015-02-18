import unittest

import mongoext.fields
import mongoext.collection
import mongoext.models


class Collection(mongoext.collection.Collection):
    CONNECTION = {'host': 'localhost', 'port': 27017}
    DATABASE = 'db1'
    NAME = 'collection1'
    KEYS_COMPRESSION = {
        'about': 'a'
    }


class Model(mongoext.models.Model):
    objects = Collection()

    about = mongoext.fields.Numeric()


class Mongoext(unittest.TestCase):
    def test_collection_find(self):
        cursor = Collection().find({'about': {'$gte': 1}}, {'about': 1}, 1).sort('about')
        self.assertTrue(all([lambda: isinstance(c, dict) for c in cursor]))

    def test_model_find(self):
        cursor = Model.objects.find({'about': {'$gte': 1}}, {'about': 1}).sort('about')
        self.assertTrue(all([lambda: isinstance(c, Model) for c in cursor]))

    def test_model_save(self):
        cursor = Model.objects.find({'about': {'$gte': 1}}, {'about': 1}).sort('about')
        model = [c for c in cursor][0]
        model.save()

    def test_model_fail_save(self):
        cursor = Model.objects.find({'about': {'$gte': 1}}, {'about': 1}).sort('about')
        model = [c for c in cursor][0]
        model.about = None
        with self.assertRaises(TypeError):
            model.save()
