from __future__ import absolute_import

import collections
import datetime

import mongoext.abc as abc
import mongoext.exc as exc


class Field(abc.AbstractField):
    def __init__(self, required=False, **kw):
        super(Field, self).__init__(**kw)

        self.required = required


class String(Field):
    def cast(self, value):
        ''' Cast valueue to String. '''
        try:
            return str(value)
        except TypeError:
            raise exc.CastError('String is required: {}'.format(value))


class Numeric(Field):
    def cast(self, value):
        ''' Cast valueue to String. '''
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exc.CastError('Integer is required: {}'.format(value))


class List(Field):
    ''' Cast valueue to list. '''
    def __init__(self, field=None, **kw):
        super(List, self).__init__(**kw)

        if field and not isinstance(field, Field):
            raise exc.SchemeError('Field successor instance required: {}'.format(field))
        self.field = field

    def cast(self, value):
        if not isinstance(value, collections.Iterable):
            raise exc.CastError('Iterable object required')
        if self.field:
            return [self.field.cast(v) for v in value]
        else:
            return list(value)


class DateTime(Field):
    def __init__(self, autoadd=False, **kw):
        super(DateTime, self).__init__(**kw)

        self.autoadd = autoadd

    def cast(self, value):
        if self.autoadd:
            value = datetime.datetime.now()
        if not isinstance(value, datetime.datetime):
            raise exc.CastError('Datetime object required')
        return value


class Dict(Field):
    def __init__(self, field=None, **kw):
        super(Dict, self).__init__(**kw)

        if field and not isinstance(field, Field):
            raise exc.SchemeError('Field successor instance required: {}'.format(field))
        self.field = field

    def cast(self, value):
        if not isinstance(value, collections.Mapping):
            raise exc.CastError('Mapping object required')
        if self.field:
            return {k: self.field.cast(v) for k, v in value.items()}
        else:
            return dict(value)
