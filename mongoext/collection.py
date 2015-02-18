from __future__ import absolute_import

import pymongo

import mongoext.cursor


class Collection(object):
    CONNECTION = None
    DATABASE = None

    KEYS_COMPRESSION = None
    NAME = None

    def __init__(self):
        self.model = None
        self.pymongo_collection = None

        if self.KEYS_COMPRESSION:
            self.keys_compression = dict(self.KEYS_COMPRESSION, _id='_id')
            self.keys_uncompression = {v: k for k, v in self.keys_compression.iteritems()}
        else:
            self.keys_compression = self.keys_uncompression = None

    @property
    def collection(self):
        if not self.pymongo_collection:
            self.pymongo_collection = pymongo.Connection(**self.CONNECTION)[self.DATABASE][self.NAME]
        return self.pymongo_collection

    def pack_fields(self, document):
        if not self.keys_compression:
            return document
        return {self.keys_compression[k]: v for k, v in document.iteritems()}

    def unpack_fields(self, document):
        if not self.keys_uncompression:
            return document
        return {self.keys_uncompression.get(k, k): v for k, v in document.iteritems()}

    def find(self, spec=None, fields=None, skip=0):
        pymongo_cursor = self.collection.find(
            spec=spec and self.pack_fields(spec),
            fields=fields and self.pack_fields(fields),
            skip=skip,
        )
        return mongoext.cursor.Cursor(self, pymongo_cursor)
