from __future__ import absolute_import

import mongoext.exc as exc


class Scheme(object):
    def __init__(self, fields):
        self.fields = fields

    def __contains__(self, field):
        return field in self.fields


class Field(object):
    def __init__(self):
        self.value = None

    def __get__(self, obj, type_):
        return self.value

    def __set__(self, obj, val):
        self.cast(val)
        self.value = val

    def cast(self, val):
        return val


class Unicode(Field):
    def cast(self, val):
        ''' Cast value to unicode. '''
        try:
            return unicode(val)
        except TypeError:
            raise exc.CastError('String is required: {}'.format(val))


class Numeric(Field):
    def cast(self, val):
        ''' Cast value to unicode. '''
        try:
            return int(val)
        except (TypeError, ValueError):
            raise exc.CastError('Integer is required: {}'.format(val))


# class List(Field):
#     def __init__(self, field=None, required=False):
#         if field and not isinstance(field, Field):
#             raise ValueError
#         self.field = field
#         self.required = required

#     def __call__(self, val):
#         if not isinstance(val, collections.Iterable):
#             raise ValueError('Iterable object required')
#         if self.field:
#             return [self.field(v) for v in val]
#         else:
#             return list(val)


# class DateTime(Field):
#     def __init__(self, required=False, autoadd=False):
#         self.required = required
#         self.autoadd = autoadd

#     def __call__(self, val):
#         if self.autoadd:
#             val = datetime.datetime.now()
#         if not isinstance(val, datetime.datetime):
#             raise ValueError('Datetime object required')
#         return val


# class Dict(Field):
#     def __init__(self, field=None, required=False):
#         if field and not isinstance(field, Field):
#             raise ValueError
#         self.field = field
#         self.required = required

#     def __call__(self, val):
#         if not isinstance(val, collections.Mapping):
#             raise ValueError('Mapping object required')
#         if self.field:
#             return {k: self.field(v) for k, v in val.items()}
#         else:
#             return dict(val)
