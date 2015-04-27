from __future__ import absolute_import

import abc
import collections

import mongoext.collection
import mongoext.scheme
import mongoext.exc


class MetaDocument(abc.ABCMeta):
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


class Document(collections.MutableMapping):
    __metaclass__ = MetaDocument
    __scheme__ = None

    _id = mongoext.scheme.Field()

    def __init__(self, **data):
        for name, value in data.items():
            if name not in self.__scheme__:
                raise mongoext.exc.SchemeError(name)
            setattr(self, name, value)

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)

    def __getitem__(self, name):
        return self.__getattribute__(name)

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)

    def __delitem__(self, name):
        return self.__delattr__(name)

    def __len__(self):
        return len(self.__scheme__)

    def __iter__(self):
        for name in self.__scheme__:
            yield name

    def __hash__(self):
        return super(object, self).__hash__()
