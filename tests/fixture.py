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


class MongoextTestCase(unittest.TestCase):
    def setUp(self):
        model = Model(about=1)
        Model.objects.insert_one(model)

    def tearDown(self):
        Collection().database.drop_collection(Collection.NAME)
