import schematec.abc
import schematec.converters
import schematec.exc
import schematec.schema
import schematec.validators

from . import exc

Schema = schematec.schema.Dictionary

Descriptor = schematec.abc.Descriptor


class Field(schematec.abc.AbstractDescriptor):
    def __call__(self, value):
        return value


Integer = schematec.converters.Integer

Number = schematec.converters.Number

String = schematec.converters.String

Required = schematec.validators.Required


def process(schema, data, weak=False):
    try:
        return schematec.schema.process(schema, data, weak=weak)
    except schematec.exc.ValidationError as e:
        raise exc.SchemaError(e)
