from __future__ import absolute_import

import mongoext.collection
import mongoext.schema
import mongoext.exc


class MetaSchema(type):
    def __new__(cls, name, bases, attrs):
        schema = {}
        for base in bases:
            for name, obj in vars(base).iteritems():
                if issubclass(type(obj), mongoext.schema.Descriptor):
                    schema[name] = obj
        for name, obj in attrs.iteritems():
            if issubclass(type(obj), mongoext.schema.Descriptor):
                schema[name] = obj
        attrs['__scheme__'] = schema
        return super(MetaSchema, cls).__new__(cls, name, bases, attrs)


class Document(object):
    __metaclass__ = MetaSchema
    __scheme__ = None

    _id = mongoext.schema.Field()

    def __init__(self, **data):
        for name, value in data.items():
            if name not in self.__scheme__:
                raise mongoext.exc.SchemeError(name)
            setattr(self, name, value)

    def __contains__(self, name):
        return name in self.__scheme__

    def __len__(self):
        return len(self.__scheme__)

    def __iter__(self):
        for name in self.__scheme__:
            yield name, getattr(self, name, None)

    def __hash__(self):
        return super(object, self).__hash__()

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)
