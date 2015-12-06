from __future__ import absolute_import

import mongoext.abc
import mongoext.collection
import mongoext.scheme
import mongoext.exc


class MetaSchema(type):
    FIELD = (mongoext.abc.AbstractField, mongoext.scheme.Field)

    def __new__(cls, class_name, bases, attrs):
        scheme = {}
        for base in bases:
            for name, obj in vars(base).iteritems():
                if issubclass(type(obj), cls.FIELD):
                    scheme[name] = obj
        for name, obj in attrs.iteritems():
            if issubclass(type(obj), cls.FIELD):
                scheme[name] = obj
        attrs['_scheme'] = scheme
        for name, field in scheme.items():
            if not isinstance(field, mongoext.abc.AbstractField):
                field = mongoext.abc.AbstractField(field)
            attrs[name] = field
        return super(MetaSchema, cls).__new__(cls, class_name, bases, attrs)


class Document(object):
    __metaclass__ = MetaSchema
    _scheme = None

    _id = mongoext.scheme.Field()

    def __init__(self, **data):
        data = mongoext.scheme.process(self._scheme, data)
        for field, value in data.items():
            setattr(self, field, value)

    def __contains__(self, name):
        return name in self._scheme

    def __len__(self):
        return len(self._scheme)

    def __iter__(self):
        for name in self._scheme:
            value = getattr(self, name, None)
            if value is not None:
                yield name, getattr(self, name, None)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)
