
import unittest

import mongoext.schema
import mongoext.collection
import mongoext.document

from . import utils


class Collection(mongoext.collection.Collection):
    CONNECTION = utils.get_connection()
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
    created_ts = mongoext.schema.Integer()


class MongoextTestCase(unittest.TestCase):
    def setUp(self):
        Collection(Document).insert_one({
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        })

    def tearDown(self):
        Collection().drop()
