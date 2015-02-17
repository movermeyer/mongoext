from __future__ import absolute_import

import pymongo

import mongoext.cursor


class Collection(object):
    CONNECTION = None
    DATABASE = None

    KEY_COMPRESSION = None
    NAME = None

    def __init__(self):
        self.model = None
        self.pymongo_collection = None

        self.KEY_UNCOMPRESSION = {v: k for k, v in self.KEY_COMPRESSION.iteritems()}

    @property
    def collection(self):
        if not self.pymongo_collection:
            self.pymongo_collection = pymongo.Connection(**self.CONNECTION)[self.DATABASE][self.NAME]
        return self.pymongo_collection

    def pack_fields(self, document):
        return {self.KEY_COMPRESSION.get(k, k): v for k, v in document.iteritems()}

    def unpack_fields(self, document):
        return {self.KEY_UNCOMPRESSION.get(k, k): v for k, v in document.iteritems()}

    def find(self, spec, fields, *args, **kw):
        if spec:
            spec = self.pack_fields(spec)
        if fields:
            fields = self.pack_fields(fields)
        pymongo_cursor = self.collection.find(spec, fields, *args, **kw)
        return mongoext.cursor.Cursor(self, pymongo_cursor)
