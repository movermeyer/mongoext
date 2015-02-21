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
        self.__pymongo_collection = None

        if self.KEYS_COMPRESSION:
            self.keys_compression = dict(self.KEYS_COMPRESSION, _id='_id')
            self.keys_uncompression = {v: k for k, v in self.keys_compression.iteritems()}
        else:
            self.keys_compression = self.keys_uncompression = None

    @property
    def collection(self):
        if not self.__pymongo_collection:
            self.__pymongo_collection = pymongo.Connection(**self.CONNECTION)[self.DATABASE][self.NAME]
        return self.__pymongo_collection

    @property
    def database(self):
        return self.collection.database

    def pack_fields(self, document):
        if not self.keys_compression:
            return document
        return {self.keys_compression[k]: v for k, v in document.iteritems()}

    def unpack_fields(self, document):
        if not self.keys_uncompression:
            return document
        return {self.keys_uncompression.get(k, k): v for k, v in document.iteritems()}

    def find(self, spec=None, fields=None, skip=0):
        ''' Query the database.

        The `spec` argument is a prototype document that all results
        must match. For example::

            db.test.find({"hello": "world"})

        only matches documents that have a key "hello" with value
        "world".  Matches can have other keys *in addition* to
        "hello". The `fields` argument is used to specify a subset of
        fields that should be included in the result documents. By
        limiting results to a certain subset of fields you can cut
        down on network traffic and decoding time.

        :param spec: (optional) a SON object specifying elements which
        must be present for a document to be included in the result set
        :type spec: dict
        '''
        pymongo_cursor = self.collection.find(
            spec=spec and self.pack_fields(spec),
            fields=fields and self.pack_fields(fields),
            skip=skip,
        )
        return mongoext.cursor.Cursor(self, pymongo_cursor)

    def insert(self, documents):
        pymongo_documents = []
        for document in documents:
            if isinstance(document, self.model):
                pymongo_documents.append(document.to_dict())
            elif isinstance(document, dict):
                pymongo_documents.append(document)
            else:
                raise TypeError(type(document))
        pymongo_documents = [self.pack_fields(d) for d in pymongo_documents]
        return self.collection.insert(pymongo_documents)

    def insert_one(self, document):
        return self.insert([document])

    def count(self):
        pass

    def create_index(self):
        pass

    def distinct(self):
        pass

    def drop(self):
        pass

    def drop_index(self):
        pass

    def drop_indexes(self):
        pass

    def ensure_index(self):
        pass

    def find_and_modify(self):
        pass

    def find_one(self):
        pass

    def full_name(self):
        pass

    def group(self):
        pass

    def remove(self):
        pass

    def save(self):
        pass

    def update(self):
        pass
