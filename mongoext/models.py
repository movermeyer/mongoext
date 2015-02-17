from __future__ import absolute_import

import mongoext.collection
import mongoext.fields


class MetaModel(type):
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
        return super(MetaModel, cls).__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        for attr, obj in vars(cls).iteritems():
            if issubclass(type(obj), mongoext.collection.Collection):
                obj.model = cls
        super(MetaModel, cls).__init__(name, bases, attrs)


class Model(object):
    __metaclass__ = MetaModel
    FIELDS = None

    _id = mongoext.fields.Field()

    def __init__(self, **kw):
        for name, obj in self.FIELDS.iteritems():
            if name in kw:
                setattr(self, name, obj(kw[name]))
            else:
                setattr(self, name, None)

    def save(self):
        self.__init__(**vars(self))

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self._id)
