from __future__ import absolute_import


def required_handler(fn):
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

    @required_handler
    def __call__(self, val):
        return val


class String(object):
    @required_handler
    def __call__(self, val):
        return unicode(val)


class Numeric(Field):
    @required_handler
    def __call__(self, val):
        return int(val)
