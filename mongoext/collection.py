from __future__ import absolute_import

import pymongo

from . import (
    cursor,
    mixin,
    scheme,
)


class Collection(mixin.FieldCompression):
    CONNECTION = None
    DATABASE = None

    NAME = None

    def __init__(self, model=None):
        self.model = model

        self.__pymongo_collection = None

    @property
    def collection(self):
        if not self.__pymongo_collection:
            self.__pymongo_collection = pymongo.MongoClient(**self.CONNECTION)[self.DATABASE][self.NAME]
        return self.__pymongo_collection

    @property
    def database(self):
        return self.collection.database

    def clean(self, document):
        for field in (f for f, v in document.items() if v is None):
            del document[field]

    def find(self, filter=None, projection=None, skip=0):
        pymongo_cursor = self.collection.find(
            filter=filter and self.pack_document(filter),
            projection=projection and self.pack_document(projection),
            skip=skip,
        )
        return cursor.Cursor(self, pymongo_cursor)

    def find_one(self, filter_or_id=None, *args, **kw):
        if isinstance(filter_or_id, dict):
            filter_or_id = self.pack_document(filter_or_id)

        document = self.collection.find_one(filter_or_id, *args, **kw)
        if not document:
            return

        document = self.unpack_document(document)
        if self.model:
            return self.model(**document)
        else:
            return document

    def find_one_and_replace(self, filter, replacement, projection=None):
        pymongo_cursor = self.collection.find_one_and_replace(
            filter=filter and self.pack_document(filter),
            replacement=replacement and self.pack_document(replacement),
            projection=projection and self.pack_document(projection),
        )
        return cursor.Cursor(self, pymongo_cursor)

    def insert(self, documents):
        pymongo_documents = map(dict, documents)
        pymongo_documents = [self.pack_document(d) for d in pymongo_documents]

        for document in pymongo_documents:
            self.clean(document)

        return self.collection.insert_many(pymongo_documents).inserted_ids

    def insert_one(self, document):
        document = dict(document)
        self.clean(document)
        document = self.pack_document(document)
        return self.collection.insert_one(document).inserted_id

    def save(self, origin):
        document = dict(origin)

        if self.model:
            scheme.verify(origin._scheme, origin)

        if document.get('_id'):
            self.find_one_and_replace(
                filter={'_id': document['_id']},
                replacement=dict(document),
            )
            _id = document['_id']
        else:
            _id = self.insert_one(document)
            if self.model:
                origin._id = _id
            else:
                origin['_id'] = _id
        return _id

    def count(self):
        return self.collection.count()

    def distinct(self, key):
        key = self.pack_field(key)
        return self.collection.distinct(key)

    def drop(self):
        return self.collection.drop()

    def remove(self, spec=None, multi=True):
        if spec is None:
            return self.collection.remove(multi=multi)

        spec = self.pack_document(spec)
        return self.collection.remove(spec, multi=multi)

    def update(self, spec, document, multi=False):
        spec = self.pack_document(spec)

        document = dict(document)
        document = self.pack_document(document)
        self.clean(document)

        self.collection.update(spec, document, multi=multi)
