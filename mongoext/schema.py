__all__ = ['Descriptor', 'Integer', 'Number', 'String']
from . import exc


class Descriptor(object):
    def __call__(self, value):
        return value


class Integer(Descriptor):
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


class Number(Descriptor):
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


class String(Descriptor):
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


class Boolean(Descriptor):
    def __call__(self, value):
        if value is None:
            raise exc.ValidationError(value)

        if isinstance(value, bool):
            return value

        if isinstance(value, (int, long)) and value in (0, 1):
            return bool(value)

        raise exc.ValidationError(value)
