class FieldCompression(object):
    FIELDS_MAPPING = None

    @classmethod
    def _mapping(cls):
        if not getattr(cls, '__mapping', None):
            cls.__mapping = dict(cls.FIELDS_MAPPING or {}, _id='_id')
        return cls.__mapping

    @classmethod
    def pack_field(cls, field):
        return cls._mapping().get(field, field)

    @classmethod
    def pack_document(cls, document):
        packed_document = {}
        for field, value in document.items():
            if not field.startswith('$'):
                field = cls.pack_field(field)
            if isinstance(value, dict):
                value = cls.pack_document(value)
            packed_document[field] = value
        return packed_document

    @classmethod
    def _reverse_mapping(cls):
        if not getattr(cls, '__reverse_mapping', None):
            cls.__reverse_mapping = {v: k for k, v in cls._mapping().items()}
        return cls.__reverse_mapping

    @classmethod
    def unpack_field(cls, field):
        return cls._reverse_mapping().get(field, field)

    @classmethod
    def unpack_document(cls, document):
        unpacked_document = {}
        for field, value in document.items():
            if not field.startswith('$'):
                field = cls.unpack_field(field)
            if isinstance(value, dict):
                value = cls.unpack_document(value)
            unpacked_document[field] = value
        return unpacked_document
