from __future__ import absolute_import


class Cursor(object):
    def __init__(self, collection, pymongo_cursor):
        self.collection = collection
        self.__pymongo_cursor = pymongo_cursor

    def sort(self, *args, **kw):
        self.__pymongo_cursor = self.__pymongo_cursor.sort(*args, **kw)
        return self

    def __iter__(self):
        for document in self.__pymongo_cursor:
            document = self.collection.unpack_fields(document)
            if self.collection.model:
                yield self.collection.model(**document)
            else:
                yield document
