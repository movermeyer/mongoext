from __future__ import absolute_import

import collections

import mongoext.collection
import mongoext.scheme
import mongoext.exc


class MetaDocument(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for base in bases:
            for name, obj in vars(base).iteritems():
                if issubclass(type(obj), mongoext.scheme.Field):
                    fields[name] = obj
        for name, obj in attrs.iteritems():
            if issubclass(type(obj), mongoext.scheme.Field):
                fields[name] = obj
        attrs['__scheme__'] = mongoext.scheme.Scheme(fields)
        return super(MetaDocument, cls).__new__(cls, name, bases, attrs)


class Document(object):
    __metaclass__ = MetaDocument
    __scheme__ = None

    _id = mongoext.scheme.Field()

    def __init__(self, **data):
        print data
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
            yield name, getattr(self, name)

    def __hash__(self):
        return super(object, self).__hash__()

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)
