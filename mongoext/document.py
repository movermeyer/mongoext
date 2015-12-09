from __future__ import absolute_import

import collections
import weakref

from . import scheme


class FieldDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data[instance]

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

    def __contains__(self, instance):
        try:
            self.data[instance]
        except KeyError:
            return False
        else:
            return True


class MetaDocument(type):
    DISCOVER = (FieldDescriptor, scheme.Field)

    def __new__(cls, class_name, bases, attrs):
        document_scheme = {}
        # collect document scheme
        for base in bases:
            for name, obj in vars(base).iteritems():
                if issubclass(type(obj), cls.DISCOVER):
                    document_scheme[name] = obj
        for name, obj in attrs.iteritems():
            if issubclass(type(obj), cls.DISCOVER):
                document_scheme[name] = obj

        # wrap all the fields into data descriptor
        for name, obj in document_scheme.items():
            if not isinstance(obj, FieldDescriptor):
                obj = FieldDescriptor(obj)
            document_scheme[name] = obj

        attrs['_scheme'] = document_scheme
        return super(MetaDocument, cls).__new__(cls, class_name, bases, attrs)


class Document(object):
    __metaclass__ = MetaDocument
    _scheme = None

    _id = scheme.Field()

    def __init__(self, **data):
        data = scheme.process(self._scheme, data)
        for field, value in data.items():
            setattr(self, field, value)

    def __getattribute__(self, name):
        scheme = super(Document, self).__getattribute__('_scheme')
        if name in scheme:
            if self in scheme[name]:
                return scheme[name].__get__(self, type(self))
            else:
                raise AttributeError(name)
        return super(Document, self).__getattribute__(name)

    def __setattr__(self, name, value):
        scheme = super(Document, self).__getattribute__('_scheme')
        if name in scheme:
            return scheme[name].__set__(self, value)
        return super(Document, self).__setattr__(name, value)

    def __delattr__(self, name):
        scheme = super(Document, self).__getattribute__('_scheme')
        if name in scheme:
            return scheme[name].__delete__(self)
        return super(Document, self).__delattr__(name)

    def __iter__(self):
        for name in (n for n in self._scheme if self in self._scheme[n]):
            yield name

    def __contains__(self, name):
        try:
            self._scheme[name].__get__(self, type(self))
        except KeyError:
            return False
        else:
            return True

    def __len__(self):
        return len(iter(self))

    def __hash__(self):
        return id(self)

    def __repr__(self):
        if '_id' in self:
            return '<{}: {}>'.format(type(self).__name__, self._id)
        else:
            return '<{}: None>'.format(type(self).__name__)

    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise KeyError(name)

    def __setitem__(self, name, value):
        return setattr(self, name, value)

    def __delitem__(self, name):
        return delattr(self, name)

    def get(self, key, default=None):
        return self[key] if key in self else default

    def iterkeys(self):
        return iter(self)

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        return (self[k] for k in self)

    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        return ((k, self[k]) for k in self)

    def items(self):
        return list(self.iteritems())

    def __eq__(self, other):
        return self is other or dict(self.items()) == dict(other.items())

    def __ne__(self, other):
        return not (self == other)

    __marker = object()

    def pop(self, key, default=__marker):
        try:
            value = self[key]
        except KeyError:
            if default is self.__marker:
                raise
            return default
        else:
            del self[key]
            return value

    def popitem(self):
        try:
            key = next(iter(self))
        except StopIteration:
            raise KeyError
        value = self[key]
        del self[key]
        return key, value

    def clear(self):
        try:
            while True:
                self.popitem()
        except KeyError:
            pass

    def update(*args, **kwds):
        if not args:
            raise TypeError('descriptor \'update\' of \'MutableMapping\' object '
                            'needs an argument')
        self = args[0]
        args = args[1:]
        if len(args) > 1:
            msg = 'update expected at most 1 arguments, got {}'.format(len(args))
            raise TypeError(msg)
        if args:
            other = args[0]
            if isinstance(other, collections.Mapping):
                for key in other:
                    self[key] = other[key]
            elif hasattr(other, 'keys'):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwds.items():
            self[key] = value

    def setdefault(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            self[key] = default
        return default
