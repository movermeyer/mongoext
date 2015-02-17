from __future__ import absolute_import


class Cursor(object):
    def __init__(self, collection, pymongo_cursor):
        self.collection = collection
        self.pymongo_cursor = pymongo_cursor

    def sort(self, *args, **kw):
        self.pymongo_cursor = self.pymongo_cursor.sort(*args, **kw)
        return self

    def __iter__(self):
        for document in self.pymongo_cursor:
            document = self.collection.unpack_fields(document)
            if self.collection.model:
                yield self.collection.model(**document)
            else:
                yield document
