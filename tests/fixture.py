
import unittest

import mongoext.scheme
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
    title = mongoext.scheme.String()
    description = mongoext.scheme.String()
    content = mongoext.scheme.String()
    created_ts = mongoext.scheme.Integer(required=True)


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
