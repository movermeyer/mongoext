from __future__ import absolute_import

import weakref

from . import scheme


class FieldDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        # every field is nullable so return None, lose empty state
        # follow common class instance behavior
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
        return instance in self.data


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
            yield name, getattr(self, name)

    def __contains__(self, name):
        return name in self._scheme and self in self._scheme[name]

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
        return (k for k, v in self)

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        return (v for k, v in self)

    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        return ((k, v) for k, v in self)

    def items(self):
        return list(self.iteritems())
