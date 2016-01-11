from __future__ import absolute_import
import pymongo

from . import abc


class AbstractClient(abc.AbstractClient):
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
