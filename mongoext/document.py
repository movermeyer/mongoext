from __future__ import absolute_import

import weakref

import mongoext.collection
import mongoext.scheme
import mongoext.exc


class AbstractField(object):
    def __init__(self, field):
        self.field = field
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance)

    def __set__(self, instance, value):
        if value is None and instance in self.data:
            del self.data[instance]
            return

        self.data[instance] = self.field(value)

    def __delete__(self, instance):
        del self.data[instance]

    def __call__(self, value):
        return self.field(value)


class MetaSchema(type):
    FIELD = (AbstractField, mongoext.scheme.Field)

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
            if not isinstance(field, AbstractField):
                field = AbstractField(field)
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
            yield name, getattr(self, name)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)
