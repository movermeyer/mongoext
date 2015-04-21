from __future__ import absolute_import

import mongoext.collection
import mongoext.fields
import mongoext.exc


class MetaDocument(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for base in bases:
            for attr, obj in vars(base).iteritems():
                if issubclass(type(obj), mongoext.fields.Field):
                    fields[attr] = obj
        for attr, obj in attrs.iteritems():
            if issubclass(type(obj), mongoext.fields.Field):
                fields[attr] = obj
        attrs['FIELDS'] = fields
        return super(MetaDocument, cls).__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        for attr, obj in vars(cls).iteritems():
            if issubclass(type(obj), mongoext.collection.Collection):
                obj._model = cls
        super(MetaDocument, cls).__init__(name, bases, attrs)


class Document(object):
    __metaclass__ = MetaDocument
    FIELDS = None

    _id = mongoext.fields.Field()

    def __init__(self, **kw):
        for name, field in self.FIELDS.iteritems():
            try:
                setattr(self, name, field(kw.get(name, mongoext.exc.Missed)))
            except ValueError as e:
                raise ValueError('{}: {}'.format(e.message, name))

    def save(self):
        self.__init__(**vars(self))

    def to_dict(self):
        return {f: getattr(self, f, None) for f in self.FIELDS}

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)