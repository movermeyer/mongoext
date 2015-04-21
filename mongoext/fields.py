from __future__ import absolute_import

import collections


def required(fn):
    def wrapper(self, val):
        if val is None:
            if self.required:
                raise ValueError(val)
            else:
                return val
        return fn(self, val)
    return wrapper


class Field(object):
    def __init__(self, required=False):
        self.required = required

    @required
    def __call__(self, val):
        return val


class String(Field):
    @required
    def __call__(self, val):
        return unicode(val)


class Numeric(Field):
    @required
    def __call__(self, val):
        return int(val)


class List(Field):
    def __init__(self, field=None, required=False):
        if field and not isinstance(field, Field):
            raise ValueError
        self.field = field
        self.required = required

    @required
    def __call__(self, val):
        if not isinstance(val, collections.Iterable):
            raise ValueError(val)
        if self.field:
            return [self.field(v) for v in val]
        else:
            return list(val)
