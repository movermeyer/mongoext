import mongoext.packages.dsnparse as dsnparse

from . import (
    interface,
    utils,
)


class AbstractCursor(object):
    def __init__(self, cursor, mapping, model):
        self._mapping = mapping
        self._model = model
        self._cursor = cursor

    def __iter__(self):
        for document in self._cursor:
            yield self._model(**self._mapping.unpack_document(document))

    def next(self):
        return self._model(**self._mapping.unpack_document(next(self._cursor)))

    __next__ = next

    def sort(self, field):
        field = self._mapping.pack_field(field)
        return type(self)(self._cursor.sort(field), self.mapping, self.model)

    def count(self):
        return self._cursor.count()

    def distinct(self, field):
        field = self._collection.mapping.pack_field(field)
        return self._cursor.distinct(field)

    def limit(self, limit):
        self._cursor = self._cursor.limit(limit)
        return self

    def rewind(self):
        self._cursor.rewind()

    def skip(self, skip):
        self._cursor = self._cursor.skip(skip)
        return self


class AbstractClient(object):
    COLLECTION_ADAPTER = interface.ICollectionAdapter
    CURSOR_ADAPTER = interface.ICursorAdapter
    CURSOR = AbstractCursor

    def __init__(self, dsn, replica_set):
        dsn = dsnparse.parse(dsn)
        database, collection = dsn.paths

        self.connection = self.connect(dsn.netlock, *(replica_set or ()))
        self.database = self.get_database(self.connection, database)
        self.collection = self.get_collection(self.database, collection)

    def get_cursor(self, cursor, mapping, model):
        return self.CURSOR(self.CURSOR_ADAPTER(cursor), mapping, model)

    @classmethod
    def connect(cls, *seeds):
        raise NotImplementedError

    @classmethod
    def get_database(cls, connection, database):
        raise NotImplementedError

    @classmethod
    def get_collection(cls, database, collection):
        raise NotImplementedError


class AbstractCollection(object):
    FIELD_MAPPER = utils.FieldMapper
    CLIENT = AbstractClient

    DSN = None
    REPLICA_SET = None

    FIELD_MAPPING = None

    def __init__(self, model):
        self.mapping = self.FIELD_MAPPER(self.FIELD_MAPPING or {})
        self.model = model
        self.client = self.CLIENT(self.DSN, self.REPLICA_SET)

    def find(self, filter_=None, projection=None, skip=0):
        filter_ = filter_ and self.mapping.pack_document(filter_)
        projection = projection and self.mapping.pack_document(projection)
        cursor = self.client.collection.find(filter_=filter_, projection=projection, skip=skip)
        return self.CURSOR(self, cursor)

    def find_one(self, filter_or_id=None, *args, **kw):
        if isinstance(filter_or_id, dict):
            filter_or_id = self.mapping.pack_document(filter_or_id)

        document = self.client.collection.find_one(filter_or_id, *args, **kw)
        if not document:
            return

        document = self.mapping.unpack_document(document)
        return self.model(**document)

    def find_one_and_replace(self, filter_, replacement, projection=None):
        filter_ = filter_ and self.mapping.pack_document(filter_)
        replacement = replacement and self.mapping.pack_document(replacement)
        projection = projection and self.mapping.pack_document(projection)

        cursor = self.client.collection.find_one_and_replace(
            filter=filter_,
            replacement=replacement,
            projection=projection,
        )
        return self.CURSOR(self, cursor)

    def insert(self, documents):
        documents = [self.mapping.pack_document(dict(d)) for d in documents]
        documents = [{f: v for f, v in d if v is not None} for d in documents]
        return self.client.collection.insert_many(documents).inserted_ids

    def insert_one(self, document):
        document = {f: v for f, v in dict(document) if v is not None}
        document = self.mapping.pack_document(document)
        return self.client.collection.insert_one(document).inserted_id

    def save(self, document):
        raise NotImplementedError

    def count(self):
        return self.client.collection.count()

    def distinct(self, field):
        field = self.mapping.pack_field(field)
        return self.client.collection.distinct(field)

    def drop(self):
        return self.client.collection.drop()

    def remove(self, spec=None, multi=True):
        if spec is None:
            return self.client.collection.remove(multi=multi)

        spec = self.mapping.pack_document(spec)
        return self.client.collection.remove(spec, multi=multi)

    def update(self, spec, document, multi=False):
        spec = self.mapping.pack_document(spec)
        document = {f: v for f, v in self.pack_document(dict(document)) if v is not None}
        self.client.collection.update(spec, document, multi=multi)
