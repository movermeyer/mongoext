from __future__ import absolute_import


class Cursor(object):
    def __init__(self, collection, pymongo_cursor):
        self.collection = collection
        self.__pymongo_cursor = pymongo_cursor

    def __iter__(self):
        for document in self.__pymongo_cursor:
            document = self.collection.unpack_fields(document)
            if self.collection._model:
                yield self.collection._model(**document)
            else:
                yield document

    def next(self):
        document = next(self.__pymongo_cursor)
        document = self.collection.unpack_fields(document)
        return document

    def sort(self, key):
        key = self.collection.pack_field(key)
        self.__pymongo_cursor = self.__pymongo_cursor.sort(key)
        return self

    def count(self):
        return self.__pymongo_cursor.count()

    def distinct(self, key):
        key = self.collection.pack_field(key)
        return self.__pymongo_cursor.distinct(key)

    def hint(self):
        pass

    def limit(self):
        pass

    def max(self):
        pass

    def max_scan(self):
        pass

    def max_time_ms(self):
        pass

    def min(self):
        pass

    def rewind(self):
        pass

    def skip(self):
        pass

    def where(self):
        pass
