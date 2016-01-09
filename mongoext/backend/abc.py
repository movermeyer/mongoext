import mongoext.packages.dsnparse as dsnparse


class FieldMapper(object):
    def __init__(self, **mapping):
        self._mapping = dict(mapping, _id='_id')
        self._reverse_mapping = {v: k for k, v in self._mapping.items()}

    def pack_field(self, field):
        return self._mapping.get(field, field)

    def pack_document(self, document):
        packed_document = {}
        for field, value in document.items():
            if not field.startswith('$'):
                field = self.pack_field(field)
            if isinstance(value, dict):
                value = self.pack_document(value)
            packed_document[field] = value
        return packed_document

    def unpack_field(self, field):
        return self._reverse_mapping.get(field, field)

    def unpack_document(self, document):
        unpacked_document = {}
        for field, value in document.items():
            if not field.startswith('$'):
                field = self.unpack_field(field)
            if isinstance(value, dict):
                value = self.unpack_document(value)
            unpacked_document[field] = value
        return unpacked_document


class AbstractConnection(object):
    @classmethod
    def connect(cls, *seeds):
        raise NotImplementedError


class AbstractDatabase(object):
    @classmethod
    def get_database(cls, connection, database):
        return connection[database]


class AbstractCursor(object):
    def __init__(self, collection, cursor):
        self._collection = collection
        self._cursor = cursor

    def __iter__(self):
        for document in self._cursor:
            document = self._collection.mapping.unpack_document(document)
            yield self._collection.model(**document)

    def next(self):
        document = next(self._cursor)
        document = self._collection.mapping.unpack_document(document)
        return self._collection.model(**document)

    __next__ = next

    def sort(self, field):
        field = self._collection.mapping.pack_field(field)
        self._cursor = self._cursor.sort(field)
        return self

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


class AbstractCollection(object):
    FIELD_MAPPER = FieldMapper
    CONNECTION = AbstractConnection
    DATABASE = AbstractDatabase
    CURSOR_WRAPPER = AbstractCursor

    DSN = None
    REPLICA_SET = None

    FIELD_MAPPING = None

    def __init__(self, model):
        dsn = dsnparse.parse(self.DSN)
        database, collection = dsn.paths

        self._connection = self.CONNECTION.connect(dsn.netlock, *(self.REPLICA_SET or ()))
        self._database = self.DATABASE.get_database(self._connection, database)
        self._collection = self.get_collection(self._database, collection)
        self.mapping = self.FIELD_MAPPER(self.FIELD_MAPPING or {})
        self.model = model

    @classmethod
    def get_collection(cls, database, collection):
        return database[collection]

    def find(self, filter_=None, projection=None, skip=0):
        cursor = self._collection.find(
            filter=filter_ and self.mapping.pack_document(filter_),
            projection=projection and self.mapping.pack_document(projection),
            skip=skip,
        )
        return self.CURSOR(self, cursor)

    def find_one(self, filter_or_id=None, *args, **kw):
        if isinstance(filter_or_id, dict):
            filter_or_id = self.mapping.pack_document(filter_or_id)

        document = self._collection.find_one(filter_or_id, *args, **kw)
        if not document:
            return

        document = self.mapping.unpack_document(document)
        return self.model(**document)

    def find_one_and_replace(self, filter_, replacement, projection=None):
        cursor = self._collection.find_one_and_replace(
            filter=filter_ and self.mapping.pack_document(filter_),
            replacement=replacement and self.mapping.pack_document(replacement),
            projection=projection and self.mapping.pack_document(projection),
        )
        return self.CURSOR(self, cursor)

    def insert(self, documents):
        documents = [self.mapping.pack_document(dict(d)) for d in documents]
        documents = [{f: v for f, v in d if v is not None} for d in documents]
        return self._collection.insert_many(documents).inserted_ids

    def insert_one(self, document):
        document = {f: v for f, v in dict(document) if v is not None}
        document = self.mapping.pack_document(document)
        return self._collection.insert_one(document).inserted_id

    def save(self, document):
        raise NotImplementedError

    def count(self):
        return self._collection.count()

    def distinct(self, field):
        field = self.mapping.pack_field(field)
        return self._collection.distinct(field)

    def drop(self):
        return self._collection.drop()

    def remove(self, spec=None, multi=True):
        if spec is None:
            return self._collection.remove(multi=multi)

        spec = self.mapping.pack_document(spec)
        return self._collection.remove(spec, multi=multi)

    def update(self, spec, document, multi=False):
        spec = self.mapping.pack_document(spec)
        document = {f: v for f, v in self.pack_document(dict(document)) if v is not None}
        self._collection.update(spec, document, multi=multi)


class AbstractDocument(object):
    pass
