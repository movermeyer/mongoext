from __future__ import absolute_import

import weakref

import mongoext.collection
import mongoext.scheme
import mongoext.exc


class FieldDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        # every field is nullable so return None, lose empty state
        return self.data.get(instance)

    def __set__(self, instance, value):
        # unset value
        if (value is None) and (instance in self.data):
            del self.data[instance]
            return

        self.data[instance] = self.field(value)

    def __delete__(self, instance):
        del self.data[instance]

    def __call__(self, value):
        return self.field(value)


class MetaDocument(type):
    DISCOVER = (FieldDescriptor, mongoext.scheme.Field)

    def __new__(cls, class_name, bases, attrs):
        scheme = {}
        # collect document scheme
        for base in bases:
            for name, obj in vars(base).iteritems():
                if issubclass(type(obj), cls.DISCOVER):
                    scheme[name] = obj
        for name, obj in attrs.iteritems():
            if issubclass(type(obj), cls.DISCOVER):
                scheme[name] = obj
        attrs['_scheme'] = scheme
        # wrap all the fields into data descriptor
        for name, obj in scheme.items():
            if not isinstance(obj, FieldDescriptor):
                obj = FieldDescriptor(obj)
            attrs[name] = obj
        return super(MetaDocument, cls).__new__(cls, class_name, bases, attrs)


class Document(object):
    __metaclass__ = MetaDocument
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
            yield name, getattr(self, name)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)
