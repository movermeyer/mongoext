from __future__ import absolute_import

import mongoext.collection
import mongoext.scheme
import mongoext.exc


class MetaDocument(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for base in bases:
            for attr, obj in vars(base).iteritems():
                if issubclass(type(obj), mongoext.scheme.Field):
                    fields[attr] = obj
        for attr, obj in attrs.iteritems():
            if issubclass(type(obj), mongoext.scheme.Field):
                fields[attr] = obj
        attrs['__scheme__'] = mongoext.scheme.Scheme(fields)
        return super(MetaDocument, cls).__new__(cls, name, bases, attrs)


class Document(object):
    __metaclass__ = MetaDocument
    __scheme__ = None

    _id = mongoext.scheme.Field()

    def __init__(self, **data):
        for attr, value in data.items():
            if attr not in self.__scheme__:
                raise mongoext.exc.SchemeError(attr)
            setattr(self, attr, value)

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__scheme__}
