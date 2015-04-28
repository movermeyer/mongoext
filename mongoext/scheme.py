from __future__ import absolute_import

import mongoext.exc as exc


class Scheme(object):
    def __init__(self, fields):
        self.fields = fields

    def __contains__(self, field):
        return field in self.fields

    def __iter__(self):
        for field in self.fields:
            yield field

    def validate(self, document):
        for attr, field in self.fields.items():
            if field.required and getattr(document, attr) is None:
                raise exc.SchemeError('Required field is missing: {}'.format(attr))
