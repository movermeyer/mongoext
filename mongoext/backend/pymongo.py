from __future__ import absolute_import
import pymongo

from . import (
    abc,
    interface,
)


class CollectionAdapter(interface.ICollectionAdapter):
    def find(self, filter_=None, projection=None, skip=0):
        return self.collection.find(filter=filter_, projection=projection, skip=skip)

    def find_one(self, filter_or_id=None, *args, **kw):
        return self.collection.find_one(filter_or_id, *args, **kw)

    def find_one_and_replace(self, filter_, replacement, projection=None):
        return self.collection.find_one_and_replace(
            filter=filter_,
            replacement=replacement,
            projection=projection,
        )

    def insert(self, documents):
        return self.collection.insert_many(documents).inserted_ids

    def insert_one(self, document):
        return self.collection.insert_one(document).inserted_id

    def save(self, document):
        raise NotImplementedError

    def count(self):
        return self.collection.count()

    def distinct(self, field):
        return self.collection.distinct(field)

    def drop(self):
        return self.collection.drop()

    def remove(self, spec=None, multi=True):
        return self.collection.remove(spec, multi=multi)

    def update(self, spec, document, multi=False):
        self.collection.update(spec, document, multi=multi)


class CursorAdapter(interface.ICursorAdapter):
    def sort(self, field):
        self.cursor = self.cursor.sort(field)

    def count(self):
        return self.cursor.count()

    def distinct(self, field):
        return self.cursor.distinct(field)

    def limit(self, limit):
        self.cursor = self.cursor.limit(limit)

    def rewind(self):
        self.cursor = self.cursor.rewind()

    def skip(self, skip):
        self.cursor =  self.cursor.skip(skip)


class AbstractClient(abc.AbstractClient):
    COLLECTION = CollectionAdapter

    @classmethod
    def connect(cls, *seeds):
        return pymongo.MongoClient(*seeds)

    @classmethod
    def get_database(cls, connection, database):
        return connection[database]

    @classmethod
    def get_collection(cls, database, collection):
        return database[collection]


class AbstractCollection(abc.AbstractCollection):
    CLIENT = AbstractClient

    def find(self, filter_=None, projection=None, skip=0):
        cursor = self._collection.find(
            filter=filter_ and self.mapping.pack_document(filter_),
            projection=projection and self.mapping.pack_document(projection),
            skip=skip,
        )
        return self.CURSOR(self, cursor)
