import unittest

import mongoext.schema
import mongoext.collection
import mongoext.document


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


class Document(mongoext.document.Document):
    title = mongoext.schema.String()
    description = mongoext.schema.String()
    content = mongoext.schema.String()
    created_ts = mongoext.schema.Integer() & mongoext.schema.Required()


class MongoextTestCase(unittest.TestCase):
    def setUp(self):
        Collection(Document).insert_one({
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        })

    def tearDown(self):
        Collection(Document).drop()
