import pymongo


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


class Collection(object):
    CONNECTION = None
    DATABASE = None

    KEY_COMPRESSION = None
    NAME = None

    def __init__(self):
        self.model = None
        self.pymongo_collection = None

        self.KEY_UNCOMPRESSION = {v: k for k, v in self.KEY_COMPRESSION.iteritems()}

    @property
    def collection(self):
        if not self.pymongo_collection:
            self.pymongo_collection = pymongo.Connection(**self.CONNECTION)[self.DATABASE][self.NAME]
        return self.pymongo_collection

    def pack_fields(self, document):
        return {self.KEY_COMPRESSION.get(k, k): v for k, v in document.iteritems()}

    def unpack_fields(self, document):
        return {self.KEY_UNCOMPRESSION.get(k, k): v for k, v in document.iteritems()}

    def find(self, spec, fields, *args, **kw):
        if spec:
            spec = self.pack_fields(spec)
        if fields:
            fields = self.pack_fields(fields)
        pymongo_cursor = self.collection.find(spec, fields, *args, **kw)
        return Cursor(self, pymongo_cursor)


class MyCollection(Collection):
    CONNECTION = {'host': 'localhost', 'port': 27017}
    DATABASE = 'db1'
    NAME = 'collection1'

    KEY_COMPRESSION = {
        'about': 'a'
    }


class Field(object):
    pass

class Raw(Field):
    def __call__(self, val):
        return val

class Numeric(Field):
    def __call__(self, val):
        return str(val)


class MetaModel(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for base in bases:
            for attr, obj in vars(base).iteritems():
                if issubclass(type(obj), Field):
                    fields[attr] = obj
        for attr, obj in attrs.iteritems():
            if issubclass(type(obj), Field):
                fields[attr] = obj
        attrs['FIELDS'] = fields
        return super(MetaModel, cls).__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        for attr, obj in vars(cls).iteritems():
            if issubclass(type(obj), Collection):
                obj.model = cls
        super(MetaModel, cls).__init__(name, bases, attrs)


class Model(object):
    __metaclass__ = MetaModel
    FIELDS = None

    _id = Raw()


class MyModel(Model):
    objects = MyCollection()

    about = Numeric()

    def __init__(self, **kw):
        for name, obj in self.FIELDS.iteritems():
            if name in kw:
                field = getattr(self, name)
                setattr(self, name, field(kw[name]))
            else:
                setattr(self, name, None)

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)

# Model.objects.find({'site_id': 1}) == [Model(), Model()]
# Collection.find() == [{'site_id': 1}, ]

if __name__ == '__main__':
    cursor = MyCollection().find({'about': {'$gte': 1}}, {'about': 1}, 1).sort('about')
    print [c for c in cursor]
    cursor = MyModel.objects.find({'about': {'$gte': 1}}, {'about': 1}, 1).sort('about')
    print [c for c in cursor]

