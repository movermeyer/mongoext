__all__ = ['Field', 'Integer', 'Number', 'String', 'Boolean']
from . import exc


class Field(object):
    def __call__(self, value):
        return value


class Integer(Field):
    def __call__(self, value):
        if value is None:
            raise exc.ValidationError(value)

        if isinstance(value, bool):
            return int(value)

        if isinstance(value, (int, long)):
            return int(value)

        if isinstance(value, basestring):
            try:
                return int(value)
            except ValueError:
                raise exc.ValidationError(value)

        raise exc.ValidationError(value)


class Number(Field):
    def __call__(self, value):
        if value is None:
            raise exc.ValidationError(value)

        if isinstance(value, bool):
            return float(value)

        if isinstance(value, (float, int, long)):
            return float(value)

        if isinstance(value, basestring):
            try:
                return float(value)
            except ValueError:
                raise exc.ValidationError(value)

        raise exc.ValidationError(value)


class String(Field):
    def __call__(self, value):
        if value is None:
            raise exc.ValidationError(value)

        if isinstance(value, unicode):
            return value

        if isinstance(value, bool):
            raise exc.ValidationError(value)

        if isinstance(value, (int, long)):
            return unicode(value)

        if isinstance(value, str):
            try:
                return unicode(value)
            except UnicodeDecodeError:
                raise exc.ValidationError(value)

        raise exc.ValidationError(value)


class Boolean(Field):
    def __call__(self, value):
        if value is None:
            raise exc.ValidationError(value)

        if isinstance(value, bool):
            return value

        if isinstance(value, (int, long)) and value in (0, 1):
            return bool(value)

        raise exc.ValidationError(value)


def process(scheme, document):
    return {k: scheme[k](v) for k, v in document.items() if k in scheme}
