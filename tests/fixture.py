import unittest

import mongoext.fields
import mongoext.collection
import mongoext.models


class Collection(mongoext.collection.Collection):
    CONNECTION = {'host': 'localhost', 'port': 27017}
    DATABASE = 'db'
    NAME = 'articles'
    KEYS_COMPRESSION = {
        'title': 't',
        'description': 'd',
        'content': 'c',
        'created_ts': 'ct',
    }


class Model(mongoext.models.Model):
    objects = Collection()

    title = mongoext.fields.String()
    description = mongoext.fields.String()
    content = mongoext.fields.String()
    created_ts = mongoext.fields.Numeric(required=True)


class MongoextTestCase(unittest.TestCase):
    def setUp(self):
        self.document = {
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        }
        Collection().insert_one(self.document)

    def tearDown(self):
        Collection().drop()
