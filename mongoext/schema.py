import schematec.abc
import schematec.schema
import schematec.converters
import schematec.validators


Schema = schematec.schema.Dictionary

Descriptor = schematec.abc.Descriptor


class Field(schematec.abc.AbstractDescriptor):
    def __call__(self, value):
        return value


Integer = schematec.converters.Integer

Number = schematec.converters.Number

String = schematec.converters.String

Required = schematec.validators.Required

process = schematec.schema.process
