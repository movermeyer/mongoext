__all__ = ['Field', 'Integer', 'Number', 'String', 'Boolean']
import six
from . import exc


class Field(object):
    def __init__(self, required=False):
        self.required = required

    def __call__(self, value):
        if value is None:
            if self.required:
                raise exc.ValidationError(value)
            else:
                return
        return value


class Integer(Field):
    def __call__(self, value):
        if value is None:
            if self.required:
                raise exc.ValidationError(value)
            else:
                return

        if isinstance(value, bool):
            return int(value)

        if isinstance(value, six.integer_types):
            return int(value)

        if isinstance(value, six.string_types):
            try:
                return int(value)
            except ValueError:
                raise exc.ValidationError(value)

        raise exc.ValidationError(value)


class Number(Field):
    def __call__(self, value):
        if value is None:
            if self.required:
                raise exc.ValidationError(value)
            else:
                return

        if isinstance(value, bool):
            return float(value)

        if isinstance(value, [float] + six.integer_types):
            return float(value)

        if isinstance(value, six.string_types):
            try:
                return float(value)
            except ValueError:
                raise exc.ValidationError(value)

        raise exc.ValidationError(value)


class String(Field):
    def __call__(self, value):
        if value is None:
            if self.required:
                raise exc.ValidationError(value)
            else:
                return

        if isinstance(value, six.string_types):
            return value

        if isinstance(value, bool):
            raise exc.ValidationError(value)

        if isinstance(value, six.integer_types):
            return six.u(value)

        if isinstance(value, six.binary_type):
            try:
                return six.u(value)
            except UnicodeDecodeError:
                raise exc.ValidationError(value)

        raise exc.ValidationError(value)


class Boolean(Field):
    def __call__(self, value):
        if value is None:
            if self.required:
                raise exc.ValidationError(value)
            else:
                return

        if isinstance(value, bool):
            return value

        if isinstance(value, six.integer_types) and value in (0, 1):
            return bool(value)

        raise exc.ValidationError(value)


def process(scheme, document):
    return {k: scheme[k](v) for k, v in document.items() if k in scheme}


def verify(scheme, document):
    return {k: scheme[k](document.get(k)) for k in scheme}
