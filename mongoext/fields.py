from __future__ import absolute_import


class Field(object):
    def __call__(self, val):
        return val


class Numeric(Field):
    def __call__(self, val):
        return str(val)
