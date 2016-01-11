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


class ICollection(object):
    def __init__(self, collection):
        self.collection = collection

    def find(self, filter_=None, projection=None, skip=0):
        raise NotImplementedError

    def find_one(self, filter_or_id=None, *args, **kw):
        raise NotImplementedError

    def find_one_and_replace(self, filter_, replacement, projection=None):
        raise NotImplementedError

    def insert(self, documents):
        raise NotImplementedError

    def insert_one(self, document):
        raise NotImplementedError

    def save(self, document):
        raise NotImplementedError

    def count(self):
        raise NotImplementedError

    def distinct(self, field):
        raise NotImplementedError

    def drop(self):
        raise NotImplementedError

    def remove(self, spec=None, multi=True):
        raise NotImplementedError

    def update(self, spec, document, multi=False):
        raise NotImplementedError


class AbstractClient(object):
    COLLECTION = ICollection

    def __init__(self, dsn, replica_set):
        dsn = dsnparse.parse(dsn)
        database, collection = dsn.paths

        self.connection = self.connect(dsn.netlock, *(replica_set or ()))
        self.database = self.get_database(self.connection, database)
        self.collection = self.get_collection(self.database, collection)

    @classmethod
    def connect(cls, *seeds):
        raise NotImplementedError

    @classmethod
    def get_database(cls, connection, database):
        raise NotImplementedError

    @classmethod
    def get_collection(cls, database, collection):
        raise NotImplementedError


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
    CLIENT = AbstractClient
    CURSOR = AbstractCursor

    DSN = None
    REPLICA_SET = None

    FIELD_MAPPING = None

    def __init__(self, model):
        self.client = self.CLIENT(self.DSN, self.REPLICA_SET)
        self.mapping = self.FIELD_MAPPER(self.FIELD_MAPPING or {})
        self.model = model

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
